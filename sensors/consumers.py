from channels.generic.websocket import WebsocketConsumer
import json
from django.core import serializers
from .models import tempature

class ChatConsumer(WebsocketConsumer):
#    groups = ["broadcast"]

    def connect(self):
        self.accept()
        message = tempature.objects.filter()
        message_serialized = serializers.serialize('json', message)
        self.send(text_data=json.dumps({
            'message': message_serialized
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
