from django.conf import settings
from pynamodb.attributes import UnicodeAttribute, JSONAttribute
from pynamodb.constants import STREAM_NEW_AND_OLD_IMAGE
from pynamodb.indexes import AllProjection

from app.models.base import BaseModel


class Sensor(BaseModel):
    class Meta:
        table_name = settings.DYNAMODB_NAME['sensor']
        region = settings.AWS_REGION_NAME
        stream_view_type = STREAM_NEW_AND_OLD_IMAGE
        projection = AllProjection()

    serial_number = UnicodeAttribute(hash_key=True)
    metadata = JSONAttribute()
