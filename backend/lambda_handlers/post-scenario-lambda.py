import logging
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, UnableToStartSession, read_decimal
from domain.scenario import Scenario
from domain.user import User
from domain.exceptions import NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType, InvalidAgeParam, MissingHomeParam, InvalidIncIncrease
from simulator import simulate_scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get the table resource
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")
    logging.info("Successfully instantiated user table resource")
    # convert the string query params to required types, return 404 on exception
    try:
        scenario_params = Scenario.get_converted_post_params(event['body'])
    except (NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType) as e:
        logger.error(e)
        return write_response(400, str(e))
    
    # pull the related user's relevant attributes from database
    user_id = event['requestContext']['authorizer']['claims']['sub']
    current_age, retirement_age, per_stock, principle = get_user_attr(user_id, table)

    # build scenario
    scenerio = Scenario(user_id)
    
    # add the given parameters to the scenario
    try:
        scenerio.append_valid_post_attr(current_age, scenario_params)
    except (InvalidAgeParam, InvalidIncIncrease, MissingHomeParam) as e:
        logger.error(e)
        return write_response(400, str(e))

    logging.info("Successfully validated parameters, calling the simulator to process the scenario")
    per_suc, best, worst, av = simulate_scenario(current_age, retirement_age, per_stock, principle, scenerio)
    scenerio.append_simulation_fields(per_suc, best, worst, av)

    logging.info("Making request to DynamoDB to place the item")
    try:
        table.put_item(Item=scenerio.to_item(),
                       ConditionExpression='attribute_not_exists(PK)')
    except ClientError as e:
        logger.error(e)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return write_response(409, f"The scenario already exists.")
        else:
            return write_response(500, "Internal error. Please try again later")
    
    logging.info("Successfully put scenario")
    return write_response_from_obj(200, scenerio.to_response())

def get_user_attr(user_id, table):
    """Get user attributes relevant to the simulation from the database
    args:
        user_id: the user id
        table: DynamoDB table resource to use in query"""
    user = User(user_id)

    attr = table.get_item(
                        Key=user.get_key(),
                        AttributesToGet=[
                            'currentAge',
                            'retirementAge',
                            'stockAllocation',
                            'principle'
                            
                        ],
                )
    
    current_age = read_decimal(attr['Item']["currentAge"])
    retirement_age = read_decimal(attr['Item']["retirementAge"])
    per_stock = read_decimal(attr['Item']["stockAllocation"])
    principle = read_decimal(attr['Item']["principle"])

    return current_age, retirement_age, per_stock, principle
    