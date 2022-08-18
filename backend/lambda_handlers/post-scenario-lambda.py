import os
import json
import logging
import uuid
from decimal import Decimal

import boto3

from backend.handler_utils.handler_utils import NoParamGiven, InvalidQueryParam, InvalidParamType, get_converted_params, write_response, get_dynamo_update_params, verify_scenario_fields, read_decimal, write_response_from_obj, InvalidAgeParam, InvalidIncIncrease
from backend.service.simulate_scenarios import simulate_scenario


logger = logging.getLogger()
logger.setLevel(logging.INFO)

POST_FIELDS = {"rent": int, 
                "food": int,
                "entertainment": int,
                "yearly_travel": int,
                "kids": int,
                "age_kids": int,
                "age_home": int,
                "home_cost": int,
                "downpayment_savings": int,
                "mortgage_rate": Decimal,
                "mortgage_length": int,
                "income_inc": list
                }


def lambda_handler(event, context):
    # read in env vars
    user_pk_prefix = os.getenv("USER_PK_PREFIX")
    scenario_pk_prefix = os.getenv("SCENARIO_PK_PREFIX")
    # get the table resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    logging.info("Successfully instantiated user table resource")
    # convert the string query params to required types, return 404 on exception
    try:
        scenario = json.loads(event['body'], parse_float = Decimal)
        scenario = get_converted_params(scenario, POST_FIELDS)
    except NoParamGiven as e:
        logger.error(e)
        return write_response(404, "At least one query parameter is required to patch the user.")
    except InvalidQueryParam as e:
        logger.error(e)
        return write_response(404, f"The parameter {e.param} is not a valid parameter.")
    except InvalidParamType as e:
        logger.error(e)
        return write_response(404, f"The parameter {e.param} cannot be converted to the required type {e.type}.")
    
    # pull the related user's relevant attributes
    pk = sk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    attr = table.get_item(
                        Key={
                        'PK': pk,
                        'SK': sk
                        },
                        AttributesToGet=[
                            'currentAge',
                            'retirementAge',
                            'stockAllocation',
                            'principle'
                            
                        ],
                )
    
    current_age = read_decimal(attr['Item']["currentAge"])
    retirement_age = read_decimal(attr['Item']["retirementAge"])
    per_stock = read_decimal(attr['Item']["stockAllocation"])
    principle = read_decimal(attr['Item']["principle"])
    
    # validate the scenario fields 
    try:
        verify_scenario_fields(current_age, scenario)
    except (InvalidAgeParam, InvalidIncIncrease) as e:
        logger.error(e)
        return write_response(404, str(e))
        
    
    logging.info("Successfully validated parameters, calling the service to process the scenarios")
    # patch the items with the given params
    # sk is updated to use uuid, partition key should be the same as the user
    sk = scenario_pk_prefix + uuid.uuid4().hex
    per_succ, best, worst, average = simulate_scenario(current_age, retirement_age, per_stock, principle, scenario)

    scenario["PK"] = pk
    scenario["SK"] = sk
    scenario["percentSuccess"] = per_succ
    scenario["best"] = best
    scenario["worst"] = worst
    scenario["average"] = average

    table.put_item(Item=scenario)
    
    logging.info(f"Successfully put scenario {pk}")
    return write_response_from_obj(201, scenario)
    