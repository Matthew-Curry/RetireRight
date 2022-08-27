import json
from decimal import Decimal
from .exceptions import NoParamGiven, InvalidQueryParam, InvalidQueryParams, InvalidParamType

def get_converted_params(query_params: str, valid_params:dict) -> dict:
    """Utility method to return given param string converted to needed types. Raises application errors if the param is invalid or type cannot be converted.
    args:
        query_params (str): the query params from the request as a string. Expected to be in JSON string format
        valid_params (dict): mapping of the same param names used in the query params to the type the field is expected to be.
    raises:
        NoParamGiven: if no query parameters are provided
        InvalidQueryParams: if the given query params is not in JSON string format
        InvalidQueryParam: if a parameter is not in the given "valid_params" dictionary
        InvalidParamType: if a parameter is not in the designated type as defined by the "valid_params" dictionary.
    output:
        returns dictionary with names of query params mapped to the values casted to the required type
    """
    
    if query_params.strip() == "":
        raise NoParamGiven()

    query_params = json.loads(query_params, parse_float = Decimal)

    if isinstance(query_params, dict) == False:
        raise InvalidQueryParams()

    for p, v in query_params.items():
        # validate the field is of the expected type
        try: 
            data_type = valid_params[p]
            # if should be set, and is list, convert
            if data_type == set and isinstance(v, list):
                v = set(v)
            if isinstance(v, data_type) == False:
                raise InvalidParamType(p, valid_params[p])
        except KeyError as e:
            raise InvalidQueryParam(p)
        except InvalidParamType as e:
            raise e
        
        query_params[p] = v
    
    return query_params
