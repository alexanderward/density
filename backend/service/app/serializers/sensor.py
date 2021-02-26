from rest_framework import serializers


from app.models.sensor import Sensor
from app.serializers.base import BaseSerializer


class SensorSerializer(BaseSerializer):

    serial_number = serializers.CharField()
    metadata = serializers.JSONField()

    class Meta:
        model = Sensor
        fields = ["serial_number", "metadata"]
