from django.db import models


class Event(models.Model):
    created = models.DateTimeField()
    img_src = models.TextField()
