from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json, requests, re
from .models import temperature
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TempSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse

def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def index(request):
    return render(request, 'sensors/index.html', {})

def pi_hole(request):
#    if mobile(request):
#        return redirect("http://192.168.0.150/admin/")
#    else:
        return render(request, 'sensors/pi-hole.html', {})

def spotify(request):
#    if mobile(request):
#        return redirect("http://home.rw:6680/iris/#")
#    else:
        return render(request, 'sensors/spotify.html', {})

def system(request):
#        return redirect("http://home.rw:19999")
#    else:
        return render(request, 'sensors/system.html', {})

@api_view(['GET', 'PUT'])
def temp_update(request):
    queryset = temperature.objects.filter()[0]
    channel_layer = get_channel_layer()
    if request.method == 'GET':
        serializer = TempSerializer(queryset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TempSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = temperature.objects.filter().values('temp', 'hum')
            async_to_sync(channel_layer.group_send)(
                "temperature", {
                    "type": "temp.message",
                    "text": json.dumps(list(message))
                }
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
