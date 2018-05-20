from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import tempature
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TempSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    return render(request, 'sensors/index.html', {})

@api_view(['GET', 'PUT'])
def temp_update(request):
    queryset = tempature.objects.filter()[0]
    channel_layer = get_channel_layer()
    if request.method == 'GET':
        serializer = TempSerializer(queryset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TempSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = tempature.objects.filter().values('temp', 'hum')
            async_to_sync(channel_layer.group_send)(
                "tempature", {"type": "broadcast.message",
                "text": json.dumps(list(message))
                }
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
