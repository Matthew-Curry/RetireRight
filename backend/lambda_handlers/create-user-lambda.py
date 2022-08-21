import os
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # read in env vars
    pk_prefix = os.getenv("PK_PREFIX")
    # get the table resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    logging.info("Successfully instantiated user table resource")

    username = event['userName']
    user_id = event['request']['userAttributes']['sub']
    pk = pk_prefix + user_id
    table.put_item(Item={'PK': pk, 'SK': pk, 'UserId': user_id, 'UserName':username})
    logging.info("Successfully put item in table")
