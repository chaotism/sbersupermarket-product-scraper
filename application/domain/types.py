from bson import ObjectId
from pydantic import PositiveInt


class IntId(PositiveInt):
    pass


class PDObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class DAO:
    pass


class Service:
    pass


class Provider:
    pass


class Repository:
    pass
