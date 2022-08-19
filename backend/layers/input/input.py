"""Utility functions related to formatting or validating the inputs to the lambda handlers"""

from .exception import InvalidQueryParam, InvalidAgeParam, InvalidIncIncrease, InvalidParamType, NoParamGiven

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

def verify_scenario_fields(current_age:int, params: dict):
    """helper method to verify the fields of a scenario. Currently will confirm
    ages make sense and income_inc is a valid data structure if provided in params
    args: 
        current_age (int): the current age attached to the user record
        params (dict): the params in the scenario object as a dicionary
    raises:
        InvalidAgeParam: if "age_kids" or "age_home" fields are provided with values less
                        than the current age.
        InvalidIncIncrease: if the income_inc is not a list of dictionaries where each dictionary
                        has keys "age" and "income" both of type int.
        """

    # given ages must be less than the current age
    if "age_kids" in params:
        if params["age_kids"] < current_age:
            raise InvalidAgeParam("age_kids", params["age_kids"], current_age)
    if "age_home" in params:
        if params["age_home"] < current_age:
            raise InvalidAgeParam("age_home", params["age_home"], current_age)

    # if income inc is given, components must be structured correctly.
    if "income_inc" in params:
        for i in params["income_inc"]:
            if isinstance(i, dict):
                if len(i.keys()) != 2:
                    raise InvalidIncIncrease
                for k, v in i.items():
                    if k != "age" and k != "income":
                        raise InvalidIncIncrease
                    if not isinstance(v, int):
                        raise InvalidIncIncrease
                        
            else:
                raise InvalidIncIncrease

def read_decimal(number):
    """Read in number as int if possible, else return. Used because DynamoDB returns all numbers as decimals"""
    if float(number)%1==0:
        return int(number)
    return number