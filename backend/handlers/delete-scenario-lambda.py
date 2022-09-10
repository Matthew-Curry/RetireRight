import logging
from botocore.exceptions import ClientError

from writer import write_response
from dynamo_utils import dynamo_resource_cache, UnableToStartSession
from domain.scenario import Scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")

    user_id = event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]
    scenario = Scenario(user_id, scenario_id)

    logging.info("Making request to DynamoDB to delete the item")
    try:
        table.delete_item(
            Key=scenario.get_key(),
            ConditionExpression='attribute_exists(PK)',
        )
    except ClientError as e:
        logger.error(e)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return write_response(404, f"No scenario with scenario id {scenario_id} exists")
        else:
            return write_response(500, "Internal error. Please try again later")

    logger.info(f"Successfully deleted scenario {scenario_id}")
    return write_response(204, "")
