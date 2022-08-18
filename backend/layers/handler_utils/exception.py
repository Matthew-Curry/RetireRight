"""Handler util exceptions"""

class BaseException(Exception):
    pass

class InvalidQueryParam(BaseException):
    def __init__(self, param):
        self.param = param
        super().__init__(f"The parameter {param} is not a valid parameter.")

class InvalidAgeParam(BaseException):
    def __init__(self, param, param_value, current_age):
        self.param = param
        super().__init__(f"The {param} value of {param_value} is lower than the current age of {current_age}")

class InvalidIncIncrease(BaseException):
    def __init__(self):
        super().__init__(f"Invalid income increase component. All components must be a map with keys age and income both of type int.")

class InvalidParamType(BaseException):
    def __init__(self, param, type):
        self.param = param
        self.type = type
        super().__init__(f"The parameter {param} cannot be converted to its required type {type}")

class NoParamGiven(BaseException):
    def __init__(self):
        super().__init__("At least one query parameter is required for this method.")