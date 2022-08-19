import os
import logging

import boto3
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # read in env vars
    user_pk_prefix = os.getenv("USER_PK_PREFIX")
    scenario_pk_prefix = os.getenv("SCENARIO_PK_PREFIX")
    # get the table resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    logger.info("Successfully instantiated user table resource")

    # delete the scenario for the given ids
    pk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]
    sk = scenario_pk_prefix + scenario_id
    
    try:
        table.delete_item(
                        Key={
                            'PK': pk,
                            'SK': sk
                            },
                        ConditionExpression='attribute_exists(PK)',
                    )
    except ClientError as e:
        logger.error(e)
        return write_response(404, f"No scenario with id {scenario_id} exists.")
                

    logger.info(f"Successfully deleted scenario {sk}")
    return write_response_from_obj(204, "")
    