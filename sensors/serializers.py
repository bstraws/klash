from rest_framework import serializers
from .models import tempature

#class TempSerializer(serializers.HyperlinkedModelSerializer):
class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = tempature
        fields = ('temp', 'hum')
