"""Domain package exceptions"""

class BaseException(Exception):
    pass

class InvalidQueryParam(BaseException):
    def __init__(self, param):
        self.param = param
        super().__init__(f"The parameter {param} is not a valid parameter.")

class InvalidQueryParams(BaseException):
    def __init__(self):
        super().__init__(f"The provided query params is not in valid JSON notation")

class InvalidAgeParam(BaseException):
    def __init__(self, param, param_value, current_age):
        self.param = param
        super().__init__(f"The {param} value of {param_value} is lower than the current age of {current_age}")

class InvalidParamType(BaseException):
    def __init__(self, param, type):
        self.param = param
        self.type = type
        super().__init__(f"The parameter {param} cannot be converted to its required type {type}")

class NoParamGiven(BaseException):
    def __init__(self):
        super().__init__("At least one query parameter is required for this method.")

# income increase errors
class InvalidIncIncrease(BaseException):
    def __init__(self):
        super().__init__(f"Invalid income increase component. The current age must be included as an integer, and all income values must be positive integers.")

class InvalidIncIncreaseTypes(InvalidIncIncrease):
    def __init__(self):
        super().__init__(f"Age and income increase values must be integers.")

class NegetiveIncomeException(InvalidIncIncrease):
    def __init__(self):
        super().__init__(f"Income increases must be positive.")

class NoCurrentIncomeException(InvalidIncIncrease):
    def __init__(self):
        super().__init__(f"Income increases must include the income of the user's current age.")

