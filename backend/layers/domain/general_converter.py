from .exceptions import NoParamGiven, InvalidQueryParam, InvalidParamType


def get_converted_params(query_params: dict, valid_params:dict) ->dict:
    """Utility method to return given params casted as needed types. Raises application errors if the param is invalid or type cannot be converted.
    args:
        query_params (dict): the query param names mapped to values from the request
        valid_params (dict): mapping of the same names used in the query params to the type the field is expected to be.
    raises:
        NoParamGiven: if no query parameters are provided
        InvalidQueryParam: if a parameter is not in the given "valid_params" dictionary
        InvalidParamType: if a parameter cannot be converted to its designated type as defined by the "valid_params" dictionary.
    output:
        returns dictionary with names of query params mapped to the values casted to the required type
    """
    if query_params == None:
        raise NoParamGiven()
        
    casted_params = {}
    for p, v in query_params.items():
        # validate the field is of the expected type
        try: 
            data_type = valid_params[p]
            v = data_type(v)
        except KeyError as e:
            raise InvalidQueryParam(p)
        except Exception as e:
            raise InvalidParamType(p, valid_params[p])
        
        casted_params[p] = v
    
    return casted_params
    