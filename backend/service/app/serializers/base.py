from rest_framework import serializers
from rest_framework.fields import ChoiceField, empty


class BaseSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )
        return self.instance

    def serialize(self):
        return self.data


class EnumField(ChoiceField):

    def __init__(self, enum, **kwargs):
        self.enum = enum
        super(EnumField, self).__init__(choices=enum.choices(), **kwargs)

    def to_representation(self, value):
        if isinstance(value, list):
            return [self.convert_to_display(x) for x in value]
        return self.convert_to_display(value)

    def convert_to_display(self, value):
        return value.name

    def run_validation(self, data=empty):
        value = super().run_validation(data)
        return self.enum[value]
