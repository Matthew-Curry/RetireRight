import logging
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, get_dynamo_update_params, UnableToStartSession
from domain.scenario import Scenario
from domain.user import User
from domain.exceptions import NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType, InvalidAgeParam, MissingHomeParam, InvalidIncIncrease
from simulator import simulate_scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        dynamodb, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")
    logging.info("Successfully instantiated user table resource")

    # convert the string request body to required types, return 400 on exception
    try:
        scenario_patch = Scenario.get_converted_patch_params(event['body'])
    except (NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType)  as e:
        logger.error(e)
        return write_response(400, str(e))
    
    user_id = event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]

    user = User(user_id)
    scenario = Scenario(user_id, scenario_id)

    # pull stored user and scenario attributes from the database to append to the objects
    try:
        # use batch get items to save network io
        response = dynamodb.batch_get_item(
                                RequestItems = {
                                            'users': {
                                                'Keys': [ user.get_key(), scenario.get_key()]
                                            }
                                        }
                                    )
    except ClientError as e:
        logger.error(e)
        return write_response(500, "Internal error. Please try again later")
    else:
        error = False
        if 'Responses' not in response:
            error = True
        elif 'users' not in response['Responses']:
            error = True
        
        if error:
            logger.warn(f"Could not find data for user {user_id}.")
            return write_response(404, f"Could not find data for user {user_id}, so the scenario could not be posted.")
    
    # loop responses and add to appropriate objects
    found_user = False
    found_scenario = False
    for result in response['Responses']['users']:
        if user.is_match(result):
            user.append_db_attr(result)
            found_user = True
        elif scenario.is_match(result):
            scenario.append_db_attr(result)
            found_scenario = True
    
    # if user does not have all fields needed for simulation, return 404
    if user.has_sim_attr() == False:
        logger.warn(f"The user {user_id} does not have all fields needed for simulation.")
        return write_response(404, f"The user {user_id} does not have all fields needed for simulation. Please patch missing fields")
    
    # if no scenario or user is found, cannot proceed
    if found_scenario == False:
        return write_response(404, f"No scenario with id {scenario_id} exists.")

    if found_user == False:
        return write_response(404, f"No user with id {user_id} exists, so the scenario could not be patched.")
    
    # apply the patch to the scenario object
    try:
        scenario.append_valid_patch_attr(user.currentAge, scenario_patch)
    except (InvalidAgeParam, InvalidIncIncrease, MissingHomeParam) as e:
        logger.error(e)
        return write_response(400, str(e))
            
    logging.info("Successfully applied patch to the scenario, starting simulation..")
    per_suc, best, worst, av = simulate_scenario(user, scenario)
    scenario.append_simulation_fields(per_suc, best, worst, av)

    dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(scenario.get_patch())
    
    logging.info("Making request to DynamoDB to patch the item")
    try:
        table.update_item(
            Key=scenario.get_key(),
            UpdateExpression=dynamo_update_exp,
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
