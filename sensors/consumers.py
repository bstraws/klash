from channels.generic.websocket import WebsocketConsumer
import json
from django.core import serializers
from .models import tempature
from asgiref.sync import async_to_sync

class tempConsumer(WebsocketConsumer):
    groups = ["tempature"]

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("tempature", self.channel_name)
        self.accept()
        message = tempature.objects.filter().values('temp', 'hum')
        self.send(json.dumps(list(message)))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("tempature", self.channel_name)

    def temp_message(self, event):
        self.send(event["text"])
