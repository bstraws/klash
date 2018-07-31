from rest_framework import serializers
from .models import temperature


class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = temperature
        fields = ('temp', 'hum')
