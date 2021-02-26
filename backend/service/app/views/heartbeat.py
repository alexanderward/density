import time

from app.serializers.heartbeat import HeartbeatSerializer
from app.views.base import BaseNoSQL, NoSQLCreateMixin, NoSQLListMixin


class HeartbeatViewset(BaseNoSQL,
                       NoSQLCreateMixin,
                       NoSQLListMixin):
    serializer_class = HeartbeatSerializer

    def filter_results(self, model):
        within = self.request.query_params.get("within")
        if within:
            return model.timestamp > int(time.time()) - int(within)
        return None
