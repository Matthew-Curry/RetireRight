import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, UnableToStartSession
from domain.user import User
from domain.scenario import Scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")

    user_id =  event['requestContext']['authorizer']['claims']['sub']
    user = User(user_id)

    # use the limit if it is passed as a query parameter, else give practically infinite limit
    if 'limit' in event["queryStringParameters"]:
        limit = event["queryStringParameters"]['limit']
    else:
        limit = 1000000000000

    logging.info("Making request to DynamoDB to get the scenarios")
    try:
        items = table.query(
                            KeyConditionExpression = Key("PK").eq(user.get_pk()),
                            FilterExpression='attribute_exists(ScenarioId)',
                            ScanIndexForward = False,
                            Limit = limit
                            )
    except ClientError as e:
        logger.error(e)
        return write_response(500, "Internal error. Please try again later")
    else:
        if 'Items' not in items:
            logger.warn(f"User {user_id} has no scenarios")
            return write_response(404, f"User {user_id} has no scnearios")
    
    # loop the scenario results and construct response
    scenarios = items['Items']
    for i, s in enumerate(scenarios):
        scenarios[i] = Scenario.from_item(s).to_response()

    logger.info(f"Successfully got scenarios for user {user_id}")
    return write_response_from_obj(200, scenarios)
    