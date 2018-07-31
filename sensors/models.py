from django.db import models
from django.utils import timezone

class temperature(models.Model):
    temp = models.IntegerField('tempature')
    hum = models.IntegerField('humidity')
