"""Holds Scenario domain object."""

from decimal import Decimal
import uuid

from .item import Item
from .exceptions import InvalidAgeParam, InvalidIncIncrease

class Scenario(Item):
    PK_PREFIX = "USER#"
    SK_PREFIX = "SCENARIO#"

    PATCH_FIELDS = {'stockAllocation': Decimal, 'retirementAge': int, 'currentAge': int, 'principle': int}
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

    def __init__(self, UserId:str, scenario_id:str = None):
        self.UserId = UserId
        # if scenario id given set, else generate uuid
        if not scenario_id:
            scenario_id = uuid.uuid4().hex

        self.PK = self.PK_PREFIX + self.UserId 
        self.SK = self.SK_PREFIX + scenario_id 

    def get_key(self) -> dict:
        """Return key of this User as dict"""
        return {'PK': self.PK, 'SK': self.PK}

    @classmethod
    def from_item(cls, item: dict):
        # construct a cls with the needed starting keys
        new_scenario = cls(item["PK"], item["SK"].removeprefix(cls.SK_PREFIX))
        item.pop("PK")
        item.pop("SK")
        # append remaining keys if valid and return
        new_scenario.append_valid_attr(item)

        return new_scenario

    def append_valid_attr(self, current_age:int, attr:dict):
        """Validate attr according to business rules, if valid, append to the instance
        params:
            attr (dict): the attributes to append
            current_age (int): the current age of the user, needed to validate the age related attributes
        raises:
            InvalidAgeParam: if "age_kids" or "age_home" fields are provided with values less
                            than the current age.
            InvalidIncIncrease: if the income_inc is not a list of dictionaries where each dictionary
                            has keys "age" and "income" both of type int.
            """
        Scenario.verify_scenario_fields(current_age, attr)
        self._append_attr(attr)

    
    @staticmethod
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
                    
    def append_simulation_fields(self, per_suc:Decimal, best:list, worst:list, av:list):
        self.percentSuccess = per_suc
        self.best = best
        self.worst = worst
        self.average = av
