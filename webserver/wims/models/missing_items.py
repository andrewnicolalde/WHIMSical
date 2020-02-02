from django.db import models

from webserver.wims.models.event import Event


class Missing_items(models.Model):
    label = models.TextField()
    event_id = models.ForeignKey(Event)
