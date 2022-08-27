import logging
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, get_dynamo_update_params, UnableToStartSession, read_decimal
from domain.scenario import Scenario
from domain.user import User
from domain.exceptions import NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType, InvalidAgeParam, InvalidIncIncrease
from simulator import simulate_scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get the service and table resources
    try:
        dynamodb, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")
    logging.info("Successfully instantiated user table resource")
    # convert the string query params to required types, return 404 on exception
    try:
        scenario_patch = Scenario.get_converted_patch_params(event['body'])
    except (NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType)  as e:
        logger.error(e)
        return write_response(400, str(e))
    
    # pull the related user's relevant attributes
    user_id = event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]

    scenario, db_scenario, current_age, retirement_age, per_stock, principle = get_inputs_from_db(user_id, scenario_id, dynamodb)
    
    # if no scenario was returned, there is nothing to update
    if db_scenario == None:
        return write_response(404, f"No scenario with id {scenario_id} exists.")
    
    # append the attrbiutes retrieved from the database
    scenario.append_db_attr(db_scenario)
    # apply the patch
    try:
        scenario.append_valid_patch_attr(current_age, scenario_patch)
    except (InvalidAgeParam, InvalidIncIncrease) as e:
        logger.error(e)
        return write_response(400, str(e))
            
    logging.info("Successfully applied patch to the scenario, starting simulation..")
    # get the simulation results and append
    per_suc, best, worst, av = simulate_scenario(current_age, retirement_age, per_stock, principle, scenario)
    scenario.append_simulation_fields(per_suc, best, worst, av)

    dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(scenario.get_patch())
    
    logging.info("Making request to DynamoDB to patch the item")
    try:
        table.update_item(
            Key=scenario.get_key(),
            UpdateExpression=dynamo_update_exp,
            # stock allocation is decimal, ages are int.
            ExpressionAttributeValues=dynamo_update_values,
            ConditionExpression='attribute_exists(PK)'
        )
    except ClientError as e:
        logger.error(e)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return write_response(404, f"The scenario does not exists.")
        else:
            return write_response(500, "Internal error. Please try again later")
    
    logging.info(f"Successfully patched scenario {scenario_id}")
    return write_response_from_obj(200, scenario.to_response())

def get_inputs_from_db(user_id, scenario_id, dynamodb):
    """helper method to retrieve the scenario and needed user attributes for the simulation
    args:
        user_id: the id of the user from the request
        scenario_id: the id of the scenario from the request
        dynamodb: the dynamodb resource
    returns:
        tuple in form (scenario, db_scenario, current_age, retirement_age, per_stock, principle)"""
    user = User(user_id)
    scenario = Scenario(user_id, scenario_id)
    # use batch get items to save network io
    response = dynamodb.batch_get_item(
                                RequestItems = {
                                            'users': {
                                                'Keys': [ user.get_key(), scenario.get_key()]
                                            }
                                        }
                                    )
    # process the items in the response to retrieve the user fields and scenario
    items = response['Responses']['users']
    db_scenario, current_age, retirement_age, per_stock, principle = process_items(items, user, scenario)
    return scenario, db_scenario, current_age, retirement_age, per_stock, principle

def process_items(items, user, scenario) -> tuple:
    """Helper method to process list of items that is expected to include
    a user and scenario object from DynamoDb. Returns the scenario and needed user fields
    args:
        items: list of dynamodb objects from query
        user: the user object expected in the list of items
        scenario: the scenario object expected in the list of items
    output:
        returns tuple in form (db_scenario, current_age, retirement_age, per_stock, principle)"""
    
    current_age = None
    retirement_age = None
    per_stock = None
    principle = None
    db_scenario = None
    for result in items:
        # is user, get current age
        if user.is_match(result):
           current_age = read_decimal(result["currentAge"])
           per_stock = read_decimal(result["stockAllocation"])
           retirement_age = read_decimal(result["retirementAge"])
           principle = read_decimal(result["principle"])
        # is processed scenario if it contains the % success
        elif scenario.is_match(result):
            db_scenario = result
    
    return db_scenario, current_age, retirement_age, per_stock, principle
    