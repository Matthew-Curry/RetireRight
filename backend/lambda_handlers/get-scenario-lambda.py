import logging
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, UnableToStartSession
from domain.scenario import Scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get the table resource
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")

    # build the scenario
    user_id =  event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]
    scenario = Scenario(user_id, scenario_id)

    logging.info("Making request to DynamoDB to get the item")
    try:
        items = table.get_item(
                            Key=scenario.get_key(),
                            )
    except ClientError as e:
        logger.error(e)
        return write_response(500, "Internal error. Please try again later")
    else:
        if 'Item' not in items:
            logger.warn(f"No scenario with id {scenario_id} exists.")
            return write_response(404, f"No scenario with id {scenario_id} exists.")
    
    # append the retrieved fields to the scenario object and return
    db_attr = items['Item']
    scenario.append_db_attr(db_attr)

    logger.info(f"Successfully got scenario {scenario_id}")
    return write_response_from_obj(200, scenario.to_response())
    