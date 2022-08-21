"""Holds User domain object."""

from decimal import Decimal
from .item import Item

class User(Item):
    PK_PREFIX = SK_PREFIX = "USER#"
    PATCH_FIELDS = {'stockAllocation': Decimal, 'retirementAge': int, 'currentAge': int, 'principle': int}
    POST_FIELDS = {'PK': str, 'SK': str, 'UserId': str, 'UserName':str}

    def __init__(self, UserId:str):
        self.UserId = UserId

        self.PK = self.PK_PREFIX + UserId
        self.SK = self.PK_PREFIX + UserId

    def get_key(self) -> dict:
        """Return key of this User as dict"""
        return {'PK': self.PK, 'SK': self.SK}

    @classmethod
    def from_item(cls, item: dict):
        # construct a cls with the needed starting keys
        new_user = cls(item["UserId"])
        item.pop("UserId")

        new_user.append_attr(item)

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
