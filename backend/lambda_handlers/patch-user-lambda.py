import logging
from botocore.exceptions import ClientError

from writer import write_response
from dynamo_utils import dynamo_resource_cache, UnableToStartSession, get_dynamo_update_params
from domain.user import User
from domain.exceptions import NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        _, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")

    # convert the string request body to required types, return 400 on exception
    try:
        params = User.get_converted_patch_params(event['body'])
    except (NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType)  as e:
        logger.error(e)
        return write_response(400, str(e))

    logging.info("Successfully validated parameters, updating item in DynamoDB")
    dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(params)
    
    user_id =  event['requestContext']['authorizer']['claims']['sub']
    user = User(user_id)
    
    logging.info("Making request to DynamoDB to patch the item")
    try:
        table.update_item(
            Key=user.get_key(),
            UpdateExpression=dynamo_update_exp,
            ExpressionAttributeValues=dynamo_update_values,
            ConditionExpression='attribute_exists(PK)'
        )
    except ClientError as e:
        logger.error(e)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return write_response(404, f"The user does not exists.")
        else:
            return write_response(500, "Internal error. Please try again later")
    
    logging.info(f"Successfully patched user {user_id}")

    return write_response(204, None)
