from django.db import models
from django.utils import timezone

class tempature(models.Model):
    temp = models.IntegerField('tempature')
    hum = models.IntegerField('humidity')
