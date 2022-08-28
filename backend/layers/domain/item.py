"""Base domain item class"""

from abc import ABC, abstractmethod
from decimal import Decimal

from .general_converter import get_converted_params

def abstractproperty(func):
   return property(classmethod(abstractmethod(func)))

class Item(ABC):

    @abstractmethod
    def get_key():
        pass
    
    @abstractmethod
    def get_pk():
        pass

    @abstractmethod
    def get_sk():
        pass

    @abstractmethod
    def from_item():
        pass

    @abstractmethod
    def to_item():
        pass

    @abstractmethod
    def to_response():
        pass

    @abstractproperty
    def PATCH_FIELDS(cls):
        pass

    @abstractproperty
    def POST_FIELDS(cls):
        pass

    @classmethod
    def get_converted_post_params(cls, query_params):
        """Wrapper on get_converted params to verify query_params against post fields"""
        return get_converted_params(query_params, cls.POST_FIELDS)
    
    @classmethod
    def get_converted_patch_params(cls, query_params):
        """Wrapper on get_converted params to verify query_params against patch fields"""
        return get_converted_params(query_params, cls.PATCH_FIELDS)
    
    def is_match(self, item: dict) -> bool:
        """Returns whether the given item is this item"""
        return item["PK"] == self.PK and item["SK"] == self.SK

    def _append_attr(self, attr:dict, is_post=True):
        """append the attributes in the given dictionary. Should only be able to append 
        valid patch or post fields. Takes parameter for whether to verify against post or patch fields.
        args:
            attr (dict): key value pairs of attributes to append to item
            is_post (bool): whether to validate against the post fields, else will valid against the patch fields"""
        for k, v in attr.items():
            if is_post:
                if k in self.POST_FIELDS and isinstance(v, self.POST_FIELDS[k]):
                    setattr(self, k, v)
            else:
                if k in self.PATCH_FIELDS and isinstance(v, self.PATCH_FIELDS[k]):
                    setattr(self, k, v)

    def append_db_attr(self, attr:dict):
        """append the attributes in the given dictionary from the DB. Allows appending post + patch fields (all valid application fields).
        Will convert numeric primitives to native Python data type as all numerics are read in as Decimal in DynamoDB
        args:
            attr (dict): key value pairs of attributes to append to item"""
        valid_fields = {**self.POST_FIELDS, **self.PATCH_FIELDS}
        for k, v in attr.items():
            if k in valid_fields:
                # if numeric that should not be a decimal appears, convert
                # to expected type for consistency
                data_type = valid_fields[k]
                if isinstance(v, Decimal) and data_type is not Decimal:
                    v = data_type(v)
                setattr(self, k, v)
