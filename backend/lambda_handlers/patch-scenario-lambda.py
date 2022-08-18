import os
import json
import logging
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
        scenario_patch = json.loads(event['body'], parse_float = Decimal)
        scenario_patch = get_converted_params(scenario_patch, POST_FIELDS)
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
    scenario_id = event['pathParameters']["scenario_id"]
    pk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    sk = scenario_pk_prefix + scenario_id
    
    # use batch get items to save network io
    items = dynamodb.batch_get_item(
                                RequestItems = {
                                            'users': {
                                                'Keys': [ 
                                                            # user
                                                            {
                                                                'PK': pk,
                                                                'SK': pk
                                                            # scenario
                                                            },
                                                            {
                                                            'PK': pk,
                                                            'SK': sk
                                                            }
                                                        ]
                                            }
                                        }
                                    )
    
    current_age = None
    retirement_age = None
    per_stock = None
    principle = None
    scenario = None
    for result in items['Responses']['users']:
        # is user, get current age
        if 'UserId' in result:
           current_age = read_decimal(result["currentAge"])
           per_stock = read_decimal(result["stockAllocation"])
           retirement_age = read_decimal(result["retirementAge"])
           principle = read_decimal(result["principle"])
        else:
            scenario = result
    
    # overwrite the scenario with the values given to patch
    for k, v in scenario_patch.items():
        scenario[k] = v
    
    # validate the scenario fields 
    try:
        verify_scenario_fields(current_age, scenario)
    except (InvalidAgeParam, InvalidIncIncrease) as e:
        logger.error(e)
        return write_response(404, str(e))
        
    
    logging.info("Successfully validated parameters, calling the service to process the scenarios")
    # patch the items with the given params
    per_succ, best, worst, average = simulate_scenario(current_age, retirement_age, per_stock, principle, scenario)

    scenario_patch["percentSuccess"] = scenario["percentSuccess"] = per_succ
    scenario_patch["best"] = scenario["best"] = best
    scenario_patch["worst"] = scenario["worst"] = worst
    scenario_patch["average"] = scenario["average"] = average

    dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(scenario_patch)
    # patch the items with the given params
    pk = sk = user_pk_prefix + event['requestContext']['authorizer']['claims']['sub']
    table.update_item(
        Key={'PK': pk, 'SK': sk},
        UpdateExpression=dynamo_update_exp,
        # stock allocation is decimal, ages are int.
        ExpressionAttributeValues=dynamo_update_values
    )
    
    logging.info(f"Successfully patched scenario {scenario_id}")
    return write_response_from_obj(200, scenario)
    