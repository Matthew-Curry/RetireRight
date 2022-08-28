"""Domain package exceptions"""

class BaseException(Exception):
    pass

class InvalidParam(BaseException):
    def __init__(self, param):
        self.param = param
        super().__init__(f"The parameter {param} is not a valid parameter.")

class InvalidRequestBody(BaseException):
    def __init__(self):
        super().__init__("The provided request body is not in valid JSON notation")

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
        super().__init__("At least one parameter must be given in the request body for this method.")

class MissingHomeParam(BaseException):
    def __init__(self, param):
        self.param = param
        super().__init__(f"If age_home param given, {param} is required.")

# income increase errors
class InvalidIncIncrease(BaseException):
    def __init__(self, err):
        super().__init__(f"Invalid income increase component. {err}")

class InvalidIncType(InvalidIncIncrease):
    def __init__(self):
        super().__init__("Income increase values must be integers.")

class InvalidIncAgeType(InvalidIncIncrease):
    def __init__(self):
        super().__init__("Ages must be castable to integers.")

class NegetiveIncomeException(InvalidIncIncrease):
    def __init__(self):
        super().__init__("Income increases must be positive.")

class NoCurrentIncomeException(InvalidIncIncrease):
    def __init__(self):
        super().__init__("Income increases must include the income of the user's current age.")

class IncomeRequiredException(InvalidIncIncrease):
    def __init__(self):
        super().__init__("Income information must be provided.")

