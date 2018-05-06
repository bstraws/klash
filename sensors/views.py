from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import tempature
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from rest_framework import status
from .serializers import TempSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    return render(request, 'sensors/index.html', {})

def room(request, room_name):
    return render(request, 'sensors/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
"""
class TempViewSet(viewsets.ModelViewSet):
    queryset = tempature.objects.filter()[0]
    serializer_class = TempSerializer
"""
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
            async_to_sync(channel_layer.group_send)(
                "broadcast", {"type": "broadcast.message",
                "text": json.dumps(serializer.data),
                }
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
