import boto3
import os
import logging

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

    # get the scenario for the given ids
    pk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]
    sk = scenario_pk_prefix + scenario_id

    items = table.get_item(
                        Key={
                        'PK': pk,
                        'SK': sk
                        }
                )
    
    if 'Item' not in items:
        logger.warn(f"No scenario with id {scenario_id} exists.")
        return write_response(404, f"No scenario with id {scenario_id} exists.")
    
    scenario = items['Item']

    logger.info(f"Successfully got scenario {sk}")
    return write_response_from_obj(200, scenario)
    