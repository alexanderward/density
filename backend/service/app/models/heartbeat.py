from django.conf import settings
from pynamodb.attributes import UnicodeAttribute, JSONAttribute, NumberAttribute
from pynamodb.constants import STREAM_NEW_AND_OLD_IMAGE
from pynamodb.indexes import AllProjection
from pynamodb_attributes import UnicodeEnumAttribute

from app.enums.states import StateEnum
from app.models.base import BaseModel


class Heartbeat(BaseModel):
    class Meta:
        table_name = settings.DYNAMODB_NAME['heartbeat']
        region = settings.AWS_REGION_NAME
        stream_view_type = STREAM_NEW_AND_OLD_IMAGE
        projection = AllProjection()

    serial_number = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)
    state = UnicodeEnumAttribute(enum_type=StateEnum)
    people_in_area = NumberAttribute()
    metadata = JSONAttribute()
