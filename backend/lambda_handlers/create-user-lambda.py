import logging

from botocore.exceptions import ClientError

from dynamo_utils import dynamo_resource_cache, UnableToStartSession
from domain.user import User

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # get the table resource
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")
    logger.info("Successfully instantiated user table resource")

    user_name = event['userName']
    user_id = event['request']['userAttributes']['sub']

    user = User(user_id, user_name)
    
    logging.info("Making request to DynamoDB to place the item")
    try:
        table.put_item(Item=user.to_item(),
                       ConditionExpression='attribute_not_exists(PK)')
    except ClientError as e:
        logger.error(e)
    else:
        logger.info("Successfully put item in table")
        return event
