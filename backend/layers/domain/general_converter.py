import json
from decimal import Decimal
from .exceptions import NoParamGiven, InvalidParam, InvalidRequestBody, InvalidParamType


def get_converted_params(request_body: str, valid_params: dict) -> dict:
    """Utility method that converts request body string to a dictionary. Validates all parameters against expected type and raises application
        errors if unexpected parameters or invalid types for parameters are encountered.
    args:
        request_body (str): the request body as a string. Expected to be in JSON string format
        valid_params (dict): mapping of the same param names used in the request body to the type the field is expected to be.
    raises:
        NoParamGiven: if the request body is empty
        InvalidRequestBody: if the given request body is not in JSON string format
        InvalidParam: if a parameter is not in the given "valid_params" dictionary
        InvalidParamType: if a parameter is not in the designated type as defined by the "valid_params" dictionary.
    output:
        returns dictionary with names of paremeters from the request body mapped to the values casted to the required type
    """

    if request_body.strip() == "":
        raise NoParamGiven

    try:
        request_body = json.loads(request_body, parse_float=Decimal)
    except Exception as e:
        raise InvalidRequestBody

    if isinstance(request_body, dict) == False:
        raise InvalidRequestBody

    # validate all fields of the request body
    for p, v in request_body.items():
        try:
            data_type = valid_params[p]
            if is_type(v, data_type) == False:
                raise InvalidParamType(p, valid_params[p])
        except KeyError as e:
            raise InvalidParam(p)
        except InvalidParamType as e:
            raise e

    return request_body


def is_type(v, data_type):
    """Helper method to check if given value matches type. Handles edge case of 
    int of 1 or 0 that should be decimal"""
    if isinstance(v, data_type):
        return True
    elif (v == 1 or v == 0) and data_type is Decimal:
        return True

    return False
