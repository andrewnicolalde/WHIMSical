from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Event(models.Model):
    created = models.DateTimeField()
    img_src = models.TextField()

class Item(models.Model):
    label = models.TextField()
    confidence = models.FloatField()
    box = JSONField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Missing_items(models.Model):
    label = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
