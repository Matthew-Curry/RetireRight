import logging
import copy
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from writer import write_response, write_response_from_obj
from dynamo_utils import dynamo_resource_cache, UnableToStartSession, get_dynamo_update_params
from domain.user import User
from domain.scenario import Scenario
from domain.exceptions import NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType, MissingUserParam, InvalidAgeParam
from simulator import simulate_scenario

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        dynamodb, table = dynamo_resource_cache.get_db_resources()
    except UnableToStartSession:
        return write_response(500, "Internal error. Please try again later")

    # convert the string request body to required types, return 400 on exception
    try:
        user_params = User.get_converted_patch_params(event['body'])
    except (NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType) as e:
        logger.error(e)
        return write_response(400, str(e))

    logging.info(
        "Successfully validated parameters. Pulling the user's scenarios from the database..")
    user_id = event['requestContext']['authorizer']['claims']['sub']
    user_params["UserId"] = user_id
    user = User(user_id)
    try:
        user.append_valid_patch_attr(user_params)
    except (MissingUserParam, InvalidAgeParam) as e:
        logger.error(e)
        return write_response(400, str(e))

    try:
        items = table.query(
            KeyConditionExpression=Key("PK").eq(user.get_pk()),
            FilterExpression='attribute_exists(ScenarioId)',
            ScanIndexForward=False,
            Limit=15
        )
    except ClientError as e:
        logger.error(e)
        return write_response(500, "Internal error. Please try again later")
    # if the user has scenarios, re-rerun the simulations with new user information
    scenarios, update_exps = get_updated_results(items, user)

    logging.info(
        "Starting a DynamoDB transaction to update the user and the scenarios..")
    try:
        dynamodb.meta.client.transact_write_items(
            TransactItems=update_exps
        )
    except ClientError as e:
        logger.error(e)
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return write_response(404, f"The user does not exists.")
        else:
            return write_response(500, "Internal error. Please try again later")

    for i, scenario in enumerate(scenarios):
        scenarios[i] = scenario.to_response()

    logger.info('Writing 200 response')
    return write_response_from_obj(200, scenarios)


def get_updated_results(items: dict, user) -> tuple:
    """Gets updated Scenario values and update expressions after re-running each Scenario's simulation
    args:
        items (dict): Result from DynamoDB query for user Scenarios
        user (User): The user that owns the scenarios
    returns:
        tuple in form (scenarios, update_expressions)"""

    update_expressions = [{'Put': {
        'TableName': 'users',
        'Item': user.to_item()
    }}]
    update_base = {'Update': {
        'TableName': 'users',
        'Key': '',
        'UpdateExpression': '',
        'ExpressionAttributeValues': '',
        'ConditionExpression': 'attribute_exists(PK)'
    }
    }
    scenarios = []
    if 'Items' in items:
        n = len(items['Items'])
        for i, data in enumerate(items['Items']):
            scenario = Scenario.from_item(data)
            scenario.update_current_age(user.currentAge)
            logger.info(f"Running simulation for scenario {i} of {n}")
            per_suc, rtc, best, worst, av = simulate_scenario(user, scenario)
            scenario.append_simulation_fields(per_suc, rtc, best, worst, av)
            scenarios.append(scenario)

            # in addition to simulation results, all variables that can change 
            # with a user age change should be updated
            dynamo_update_exp, dynamo_update_values = get_dynamo_update_params(
                {'percentSuccess': scenario.percentSuccess,
                'retirementTotalCost': scenario.retirementTotalCost,
                 'best': scenario.best,
                 'worst': scenario.worst,
                 'average': scenario.average,
                 'ageKids': scenario.ageKids,
                 'incomeInc': scenario.incomeInc,
                 'ageHome': scenario.ageHome,
                 'homeCost': scenario.homeCost,
                 'downpaymentSavings': scenario.downpaymentSavings,
                 'mortgageRate': scenario.mortgageRate,
                 'mortgageLength': scenario.mortgageLength
                 })
            exp = copy.deepcopy(update_base)
            exp['Update']['Key'] = scenario.get_key()
            exp['Update']['UpdateExpression'] = dynamo_update_exp
            exp['Update']['ExpressionAttributeValues'] = dynamo_update_values
            update_expressions.append(exp)

    if scenarios:
        logger.info(f"Ran simualations for {len(scenarios)} scenarios.")

    return scenarios, update_expressions
