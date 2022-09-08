"""Holds Scenario domain object."""

from decimal import Decimal
import uuid
import time

from .item import Item
from .exceptions import (InvalidAgeParam, MissingHomeParam, InvalidIncAgeType, InvalidIncType, 
    NegetiveIncomeException, NoCurrentIncomeException, IncomeRequiredException, IncRepeatedAge)

class Scenario(Item):
    PK_PREFIX = "USER#"
    SK_PREFIX = "SCENARIO#"

    PATCH_FIELDS = POST_FIELDS = {"rent": int, 
                                    "food": int,
                                    "entertainment": int,
                                    "yearlyTravel": int,
                                    "ageKids": list,
                                    "ageHome": int,
                                    "homeCost": int,
                                    "downpaymentSavings": int,
                                    "mortgageRate": Decimal,
                                    "mortgageLength": int,
                                    "incomeInc": dict
                                }
    
    PROCESSED_FIELDS = {
        "percentSuccess": Decimal,
        "best": list,
        "worst": list,
        "average": list
    }

    def __init__(self, user_id:str, scenario_id:str = None):
        # if scenario id given set, else generate id that is timestamp + uuid
        if not scenario_id:
            scenario_id = str(int(time.time())) + uuid.uuid4().hex
        
        self.ScenarioId = scenario_id

        self.PK = self.PK_PREFIX + user_id
        self.SK = self.SK_PREFIX + scenario_id 

        # intiialize all attrbiutes to 0 values, other than incomeInc which is a required parameter
        self.rent = 0
        self.food = 0
        self.entertainment = 0
        self.yearlyTravel = 0
        self.ageKids = []
        self.ageHome = None
        self.homeCost = 0
        self.downpaymentSavings = 0
        self.mortgageRate = 0
        self.mortgageLength = 0

        # initialize patch to none
        self.patch = None

    def get_key(self) -> dict:
        """Return key of this Scenario as dict"""
        return {'PK': self.PK, 'SK': self.SK}
    
    def get_pk(self):
        return self.PK

    def get_sk(self):
        return self.SK
    
    def get_patch(self) -> dict:
        """Returns the most recent patch applied to the Scenario."""
        return self.patch

    @classmethod
    def from_item(cls, item: dict):
        # construct a cls with the needed starting keys
        new_scenario = cls(item["PK"].removeprefix(cls.SK_PREFIX), item["SK"].removeprefix(cls.SK_PREFIX))
        item.pop("PK")
        item.pop("SK")
        # append remaining keys if valid and return
        new_scenario.append_db_attr(item)

        return new_scenario

    def append_valid_post_attr(self, current_age:int, attr:dict):
        """Validate attr according to business rules, if valid, append to the instance if valid post fields
        params:
            attr (dict): the attributes to append
            current_age (int): the current age of the user, needed to validate the age related attributes
        raises:
            InvalidAgeParam: if age of having a kid, buying a home, or increasing income 
                            are provided with values less than the current age.
            InvalidIncAgeType: if age key in incomeInc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if ageHome is provided but one of the required params
                            homeCost, mortgageRate, or mortgageLength is missing.
            """
        Scenario.verify_scenario_fields(current_age, attr)
        self._append_attr(attr)
    
    def append_valid_patch_attr(self, current_age:int, attr:dict):
        """Validate attr according to business rules, if valid, append to the instance is valid patch fields.
        Scenario object will also store the patch attributes which can be retrieved for a dynamodb update query.
        params:
            attr (dict): the attributes to append
            current_age (int): the current age of the user, needed to validate the age related attributes
        raises:
            InvalidAgeParam: if age of having a kid, buying a home, or increasing income 
                            are provided with values less than the current age.
            InvalidIncAgeType: if age key in incomeInc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if ageHome is provided but one of the required params
                            homeCost, mortgageRate, or mortgageLength is missing.
            """
        # verify patch attributes alongside current attributes
        patch = attr
        merged_fields = {**self.__dict__, **attr}
        Scenario.verify_scenario_fields(current_age, merged_fields)
        # append the patch and store patched fields in instance variable
        self._append_attr(patch, is_post=False)
        self.patch = patch

    @staticmethod
    def verify_scenario_fields(current_age:int, params: dict):
        """helper method to verify the fields of a scenario. Currently will confirm
        ages and combination of home params follow business rules and incomeInc is a 
        valid data structure if provided in params.
        args: 
            current_age (int): the current age attached to the user record
            params (dict): the params in the scenario object as a dicionary
        raises:
            InvalidAgeParam: if age of having a kid, buying a home, or increasing income 
                            are provided with values less than the current age.
            InvalidIncAgeType: if age key in incomeInc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if ageHome is provided but one of the required params
                            homeCost, mortgageRate, or mortgageLength is missing.
            """

        # the age the user plans to buy a home must be after the current age. Also, 
        # if an age of home purchase is provided, a homeCost, mortgageRate, and
        # mortgageLength must also be provided.
        if "ageHome" in params:
            if params["ageHome"]:
                if params["ageHome"] < current_age:
                    raise InvalidAgeParam("ageHome", params["ageHome"], current_age)

                if "homeCost" not in params:
                    raise MissingHomeParam("homeCost")

                if "mortgageRate" not in params:
                    raise MissingHomeParam("mortgageRate")

                if "mortgageLength" not in params:
                    raise MissingHomeParam("mortgageLength")
        
        # the ages the user plans to have kids must be after the current age
        if "ageKids" in params:
            for age in params["ageKids"]:
                if age < current_age:
                    raise InvalidAgeParam("ageKids", age, current_age)

        # if income inc is given, current age must be included, all other ages must be greater than the current age, 
        # and all income values must be positive integers. Income information must be provided.
        found_current_age = False
        if "incomeInc" in params:
            income_inc = params["incomeInc"]

            # keys must be unique
            if len(income_inc) != len(set(income_inc.values())):
                raise IncRepeatedAge

            for k, v in income_inc.items():
                try:
                    k = int(k)
                except Exception as e:
                    raise InvalidIncAgeType
                
                # value can be a decimal (if incoming from DB) but must not have places beyond decimal
                # (conform to being an int)
                if isinstance(v, Decimal):
                    if v.as_tuple().exponent != 0:
                        raise InvalidIncType
                elif isinstance(v, int) == False:
                    raise InvalidIncType

                if k < current_age:
                    raise InvalidAgeParam("incomeInc", k, current_age)
                elif k == current_age:
                    found_current_age = True
                
                if v < 0:
                    raise NegetiveIncomeException
            
            if found_current_age == False:
                raise NoCurrentIncomeException
        else:
            raise IncomeRequiredException
                    
    def append_simulation_fields(self, per_suc:Decimal, best:list, worst:list, av:list):
        """Used as entrypoint to add simulation result fields to an already constructed scenario"""
        self.percentSuccess = per_suc
        self.best = best
        self.worst = worst
        self.average = av
    
    def to_item(self) -> dict:
        """Convert item into dynamodb compatible key value pairs"""
        item_fields = self.__dict__.copy()
        if "patch" in item_fields:
            item_fields.pop("patch")
        return item_fields

    def to_response(self) -> dict:
        """Convert item into key value pairs for the response"""
        # pop non application fields
        public_fields = self.__dict__.copy()
        if "PK" in public_fields:
            public_fields.pop("PK")
        if "SK" in public_fields:
            public_fields.pop("SK")
        if "patch" in public_fields:
            public_fields.pop("patch")

        return public_fields
