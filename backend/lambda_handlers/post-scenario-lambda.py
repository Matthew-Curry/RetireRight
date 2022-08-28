import logging
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, UnableToStartSession
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
    # convert the string query params to required types, return 400 on exception
    try:
        scenario_params = Scenario.get_converted_post_params(event['body'])
    except (NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType) as e:
        logger.error(e)
        return write_response(400, str(e))
    
    # pull the related user's relevant attributes from database into a user object
    user_id = event['requestContext']['authorizer']['claims']['sub']
    user = User(user_id)
    try:
        attr = table.get_item(
                        Key=user.get_key(),
                        AttributesToGet=[
                            'currentAge',
                            'retirementAge',
                            'stockAllocation',
                            'principle'
                            
                        ],
                )
    except ClientError as e:
        logger.error(e)
        return write_response(500, "Internal error. Please try again later")
    else:
        if 'Item' not in attr:
            logger.warn(f"No user with id {user_id} exists.")
            return write_response(404, f"No user with id {user_id} exists, so the scenario could not be posted.")
    
    user.append_db_attr(attr['Item'])

    # build scenario
    scenerio = Scenario(user_id)
    
    # add the given parameters to the scenario
    try:
        scenerio.append_valid_post_attr(user.current_age, scenario_params)
    except (InvalidAgeParam, InvalidIncIncrease, MissingHomeParam) as e:
        logger.error(e)
        return write_response(400, str(e))

    logging.info("Successfully validated parameters, calling the simulator to process the scenario")
    per_suc, best, worst, av = simulate_scenario(user, scenerio)
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
