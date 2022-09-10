"""Holds User domain object."""

from decimal import Decimal
from .item import Item
from .exceptions import InvalidAgeParam, MissingUserParam


class User(Item):
    PK_PREFIX = SK_PREFIX = "USER#"
    PATCH_FIELDS = {'UserName': str, 'stockAllocation': Decimal,
                    'retirementAge': int, 'currentAge': int, 'principle': int}
    POST_FIELDS = {'UserName': str}
    PROCESSED_FIELDS = {}

    def __init__(self, UserId: str, UserName=None):
        self.UserId = UserId
        self.UserName = UserName

        self.PK = self.PK_PREFIX + UserId
        self.SK = self.PK_PREFIX + UserId

    def get_key(self) -> dict:
        """Return key of this User as dict"""
        return {'PK': self.PK, 'SK': self.SK}

    def get_pk(self):
        return self.PK

    def get_sk(self):
        return self.SK

    def has_sim_attr(self) -> bool:
        """returns whether the user instance has all fields needed to run a simulation (the PATCH fields)"""
        for field in self.PATCH_FIELDS:
            if field not in self.__dict__:
                return False

        return True

    @classmethod
    def from_item(cls, item: dict):
        # construct a cls with the needed starting keys
        new_user = cls(item["UserId"])
        item.pop("UserId")

        new_user.append_db_attr(item)

        return new_user

    def to_item(self) -> dict:
        """Convert item into dynamodb compatible key value pairs"""
        return self.__dict__

    def to_response(self) -> dict:
        """Convert item into key value pairs for the response"""
        # pop non application fields
        public_fields = self.__dict__.copy()
        if "PK" in public_fields:
            public_fields.pop("PK")
        if "SK" in public_fields:
            public_fields.pop("SK")

        return public_fields

    def append_valid_patch_attr(self, attr: dict):
        """Validate patch attributes and if valid, append
        args:
            attr (dict): the attributes to append
        raises: 
            InvalidAgeParam: if the retirement age exceeds the current age
            MissingUserParam: if required param is missing
        """
        self.verify_user_fields(attr)
        self._append_attr(attr, False)

    def verify_user_fields(self, attr: dict):
        """helper method to verify the given fields to create a user are valid
        args:
            attr (dict): the attributes to check
        raises: 
            InvalidAgeParam: if the retirement age exceeds the current age
            MissingUserParam: if required param is missing
        """
        for field in self.PATCH_FIELDS.keys():
            if field not in attr.keys():
                raise MissingUserParam(field)

        if attr['retirementAge'] < attr['currentAge']:
            raise InvalidAgeParam(
                'retirementAge', attr['retirementAge'], attr['currentAge'])
