from channels.generic.websocket import WebsocketConsumer
import json, requests
from django.core import serializers
from .models import temperature
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class tempConsumer(WebsocketConsumer):
    groups = ["temperature"]
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("temperature", self.channel_name)
        self.accept()
        message = temperature.objects.filter().values('temp', 'hum')
        self.send(json.dumps(list(message)))
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("temperature", self.channel_name)
    def temp_message(self, event):
        self.send(event["text"])

class forecastConsumer(WebsocketConsumer):
    groups = ["forecast"]

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("forecast", self.channel_name)
        self.accept()
        channel_layer = get_channel_layer()
        secret_key = ''
        location = '39.9366,-82.8786'
        limit = {'exclude': '[minutely,hourly,alerts,flags]'}
        r = requests.get("https://api.darksky.net/forecast/{0}/{1}"
            .format(secret_key, location), params=limit)
        weather = r.text
        print(r.text)
        async_to_sync(channel_layer.group_send)(
            "forecast", {"type": "forecast.message",
            "text": weather
            }
        )
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("forecast", self.channel_name)

    def receive(self, text_data):
        channel_layer = get_channel_layer()
        secret_key = ''
        location = '39.9366,-82.8786'
        limit = {'exclude': '[minutely,hourly,alerts,flags]'}
        r = requests.get("https://api.darksky.net/forecast/{0}/{1}"
            .format(secret_key, location), params=limit)
        weather = r.text
        async_to_sync(channel_layer.group_send)(
            "forecast", {
                "type": "forecast.message",
                "text": weather
            }
        )
    def forecast_message(self, event):
        self.send(event["text"])
