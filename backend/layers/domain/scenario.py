"""Holds Scenario domain object."""

from decimal import Decimal
import uuid

from .item import Item
from .exceptions import InvalidAgeParam, MissingHomeParam, InvalidIncAgeType, InvalidIncType, NegetiveIncomeException, NoCurrentIncomeException

class Scenario(Item):
    PK_PREFIX = "USER#"
    SK_PREFIX = "SCENARIO#"

    PATCH_FIELDS = POST_FIELDS = {"rent": int, 
                                    "food": int,
                                    "entertainment": int,
                                    "yearly_travel": int,
                                    "age_kids": list,
                                    "age_home": int,
                                    "home_cost": int,
                                    "downpayment_savings": int,
                                    "mortgage_rate": Decimal,
                                    "mortgage_length": int,
                                    "income_inc": dict
                                    }

    def __init__(self, UserId:str, scenario_id:str = None):
        # if scenario id given set, else generate uuid
        if not scenario_id:
            scenario_id = uuid.uuid4().hex
        
        self.ScenarioId = scenario_id

        self.PK = self.PK_PREFIX + UserId
        self.SK = self.SK_PREFIX + scenario_id 

        # intiialize all attrbiutes to 0 values
        self.rent = 0
        self.food = 0
        self.entertainment = 0
        self.yearly_travel = 0
        self.age_kids = []
        self.age_home = None
        self.home_cost = 0
        self.downpayment_savings = 0
        self.mortgage_rate = 0
        self.mortgage_length = 0
        self.income_inc = {}

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
        new_scenario = cls(item["PK"], item["SK"].removeprefix(cls.SK_PREFIX))
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
            InvalidIncAgeType: if age key in income_inc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if age_home is provided but one of the required params
                            home_cost, mortgage_rate, or mortgage_length is missing.
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
            InvalidIncAgeType: if age key in income_inc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if age_home is provided but one of the required params
                            home_cost, mortgage_rate, or mortgage_length is missing.
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
        ages and combination of home params make sense and income_inc is a valid data 
        structure if provided in params.
        args: 
            current_age (int): the current age attached to the user record
            params (dict): the params in the scenario object as a dicionary
        raises:
            InvalidAgeParam: if age of having a kid, buying a home, or increasing income 
                            are provided with values less than the current age.
            InvalidIncAgeType: if age key in income_inc is not castable to an integer
            InvalidIncType: if income increase is not an integer
            NegetiveIncomeException: if a negetive income value is provided
            NoCurrentIncomeException: if income at current age is not provided
            MissingHomeParam: if age_home is provided but one of the required params
                            home_cost, mortgage_rate, or mortgage_length is missing.
            """

        # the age the user plans to buy a home must be after the current age. Also, 
        # if an age of home purchase is provided, a home_cost, mortgage_rate, and
        # mortgage_length must also be provided.
        if "age_home" in params:
            if params["age_home"] < current_age:
                raise InvalidAgeParam("age_home", params["age_home"], current_age)

            if "home_cost" not in params:
                raise MissingHomeParam("home_cost")

            if "mortgage_rate" not in params:
                raise MissingHomeParam("mortgage_rate")

            if "mortgage_length" not in params:
                raise MissingHomeParam("mortgage_length")
        
        # the ages the user plans to have kids must be after the current age
        if "age_kids" in params:
            for age in params["age_kids"]:
                if age < current_age:
                    raise InvalidAgeParam("age_kids", params["age_kids"], current_age)

        # if income inc is given, current age must be included, all other ages must be greater than the current age, 
        # and all income values must be positive
        found_current_age = False
        if "income_inc" in params:
            for k, v in params["income_inc"].items():
                try:
                    k = int(k)
                except Exception as e:
                    raise InvalidIncAgeType
                
                if isinstance(v, int) == False:
                    raise InvalidIncType

                if k < current_age:
                    raise InvalidAgeParam("income_inc", k, current_age)
                elif k == current_age:
                    found_current_age = True
                
                if v < 0:
                    raise NegetiveIncomeException
            
            if found_current_age == False:
                raise NoCurrentIncomeException
                    
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
