import os
import json
import logging
from decimal import Decimal

import boto3

from backend.handler_utils.handler_utils import NoParamGiven, InvalidQueryParam, InvalidParamType, get_converted_params, write_response, get_dynamo_update_params

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PATCH_FIELDS = {'stockAllocation': Decimal, 'retirementAge': int, 'currentAge': int, 'principle': int}

def lambda_handler(event, context):
    # read in env vars
    pk_prefix = os.getenv("PK_PREFIX")
    # get the table resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    logging.info("Successfully instantiated user table resource")
    # convert the string query params to required types, return 404 on exception
    try:
        params = json.loads(event['body'], parse_float = Decimal)
        params = get_converted_params(params, PATCH_FIELDS)
    except NoParamGiven as e:
        logger.error(e)
        return write_response(404, "At least one query parameter is required to patch the user.")
    except InvalidQueryParam as e:
        logger.error(e)
        return write_response(404, f"The parameter {e.param} is not a valid parameter.")
    except InvalidParamType as e:
        logger.error(e)
        return write_response(404, f"The parameter {e.param} cannot be converted to the required type {e.type}.")

    logging.info("Successfully validated parameters, updating item in DynamoDB")
    dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(params)
    # patch the items with the given params
    pk = sk = pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    table.update_item(
        Key={'PK': pk, 'SK': sk},
        UpdateExpression=dynamo_update_exp,
        # stock allocation is decimal, ages are int.
        ExpressionAttributeValues=dynamo_update_values
    )
    
    logging.info(f"Successfully patched user {pk}")

    return write_response(204, None)
