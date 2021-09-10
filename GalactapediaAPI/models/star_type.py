from django.db.models.deletion import SET_NULL
from django.db import models


class StarType(models.Model):
    type = models.CharField(max_length=10)
