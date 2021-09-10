from django.db.models.deletion import SET_NULL
from django.db import models


class Asteroid(models.Model):
    stellar_object_id = models.ForeignKey("stellarobject", on_delete=models.CASCADE)