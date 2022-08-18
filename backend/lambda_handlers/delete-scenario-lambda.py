import boto3
import os
import logging

from backend.handler_utils.handler_utils import write_response_from_obj

def lambda_handler(event, context):
    # read in env vars
    user_pk_prefix = os.getenv("USER_PK_PREFIX")
    scenario_pk_prefix = os.getenv("SCENARIO_PK_PREFIX")
    # get the table resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    logging.info("Successfully instantiated user table resource")

    # delete the scenario for the given ids
    pk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    scenario_id = event['pathParameters']["scenario_id"]
    sk = scenario_pk_prefix + scenario_id

    table.delete_item(
                    Key={
                    'PK': pk,
                    'SK': sk
                    }
                )

    logging.info(f"Successfully deleted scenario {sk}")
    return write_response_from_obj(204, "")
    