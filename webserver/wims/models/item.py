from django.contrib.postgres.fields import JSONField
from django.db import models

from webserver.wims.models.event import Event


class Item(models.Model):
    label = models.TextField()
    confidence = models.FloatField()
    box = JSONField()
    event_id = models.ForeignKey(Event)
