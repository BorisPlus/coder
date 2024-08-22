import os
import sys
from typing import Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sv.params import Params as ParamsClassFromSvExample


class BaseParams:
    def __new__(cls, **kwargs):
        if getattr(cls, "__fields__", None) is None:
            raise Exception(f"__fields__ not defined in class {cls}")
        if getattr(cls, "deserialization_object_from_fields", None) is None:
            raise Exception(
                f"classmethod deserialization_object_from_fields() not defined in class {cls}"
            )
        return super().__new__(cls)

    @classmethod
    def deserialization_object_from_fields(cls, fields_values):
        kwargs = dict()
        for i in range(0, len(fields_values)):
            kwargs[getattr(cls, "__fields__", [])[i]] = fields_values[i]
        return cls(**kwargs)

    def fields_for_object_serialization(self) -> tuple:
        return tuple(
            getattr(self, x) for x in getattr(self.__class__, "__fields__", [])
        )

    def __str__(self) -> str:
        return str(self.fields_for_object_serialization())


class Params(BaseParams, ParamsClassFromSvExample):
    __fields__ = ("number", "string", "raw_bytes")
