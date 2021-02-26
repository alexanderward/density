from app.serializers.sensor import SensorSerializer
from app.views.base import BaseNoSQL, NoSQLCreateMixin, NoSQLListMixin


class SensorViewset(BaseNoSQL,
                    NoSQLCreateMixin,
                    NoSQLListMixin):
    serializer_class = SensorSerializer
