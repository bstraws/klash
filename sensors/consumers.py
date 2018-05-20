from channels.generic.websocket import WebsocketConsumer
import json
from django.core import serializers
from .models import tempature
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("broadcast", self.channel_name)
        self.accept()
        message = tempature.objects.filter().values('temp', 'hum')
#        message_serialized = serializers.serialize('json', message)
        self.send(json.dumps(list(message)))
#        self.send(text_data=json.dumps({
#            'message': message_serialized
#        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("broadcast", self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
    def broadcast_message(self, event):
        self.send(event["text"])
