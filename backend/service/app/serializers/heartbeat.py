from rest_framework import serializers
from app.enums.states import StateEnum
from app.models.heartbeat import Heartbeat
from app.serializers.base import BaseSerializer, EnumField


class HeartbeatSerializer(BaseSerializer):
    serial_number = serializers.CharField()
    timestamp = serializers.IntegerField()
    state = EnumField(StateEnum)
    people_in_area = serializers.IntegerField()
    metadata = serializers.JSONField()

    class Meta:
        model = Heartbeat
        fields = ["serial_number", "timestamp", "state", "metadata", "people_in_area"]
