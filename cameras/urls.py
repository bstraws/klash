from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.camera_01, name='01'),
]
