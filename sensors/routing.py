from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/sensors/temp$', consumers.tempConsumer),
    url(r'^ws/sensors/forecast$', consumers.forecastConsumer),
]
