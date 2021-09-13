from django.db.models.deletion import SET_NULL
from django.db import models


class Star_Type(models.Model):
    type = models.CharField(max_length=10)
