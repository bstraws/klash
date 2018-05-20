from django.conf.urls import  url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('temp_update', views.temp_update, name='temp_update'),
]
