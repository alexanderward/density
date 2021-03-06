import enum
import random


def value_equals_enum(value, enum_object):
    return value == enum_object.name


def value_in_enums(value, enum_objects):
    return any([value_equals_enum(value, x) for x in enum_objects])


class BaseEnum(enum.Enum):

    @classmethod
    def name_in_enum(cls, name):
        return name in cls.get_names()

    @classmethod
    def value_in_enum(cls, value):
        return value in cls.get_values()

    @classmethod
    def get_names(cls):
        return [x.name for x in cls if x.name if not x.name.islower()]

    @classmethod
    def get_values(cls):
        return [x.value for x in cls]

    @classmethod
    def serialize(cls):
        return cls.name

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_random(cls):
        return random.choice(cls.get_names())
