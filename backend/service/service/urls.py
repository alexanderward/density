from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from app.views.heartbeat import HeartbeatViewset
from app.views.sensor import SensorViewset

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewset, basename="sensors")
router.register(r'heartbeats', HeartbeatViewset, basename="heartbeats")

urlpatterns = [
    url(r'^', include(router.urls))
]
