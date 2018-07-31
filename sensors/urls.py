from django.conf.urls import  url

from . import views

urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url('temp_update', views.temp_update, name='temp_update'),
    url('pi-hole', views.pi_hole, name='pi-hole'),
    url('spotify', views.spotify, name='spotify'),
    url('system', views.system, name='system'),
]
