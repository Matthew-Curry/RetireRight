"""Base item class"""

from abc import ABC, abstractmethod

from .general_converter import get_converted_params

def abstractproperty(func):
   return property(classmethod(abstractmethod(func)))

class Item(ABC):

    @abstractmethod
    def get_key():
        pass

    @abstractmethod
    def from_item():
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

    def _append_attr(self, attr:dict):
        """append the attributes in the given dictionary. Should only be able to append 
        valid patch or post fields."""
        for k, v in attr.items():
            if (k in self.POST_FIELDS or k in self.PATCH_FIELDS) and isinstance(v, self.POST_FIELDS[k]):
                setattr(self, k, v)

    def to_dict(self) -> dict:
        """Convert item into key value pairs"""
        return self.__dict__
