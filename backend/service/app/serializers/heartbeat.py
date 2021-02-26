from rest_framework import serializers
from rest_framework.fields import ChoiceField, empty

from app.enums.states import StateEnum
from app.models.heartbeat import Heartbeat
from app.serializers.base import BaseSerializer


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


class HeartbeatSerializer(BaseSerializer):
    serial_number = serializers.CharField()
    timestamp = serializers.IntegerField()
    state = EnumField(StateEnum)
    metadata = serializers.JSONField()

    class Meta:
        model = Heartbeat
        fields = ["serial_number", "timestamp", "state", "metadata"]
