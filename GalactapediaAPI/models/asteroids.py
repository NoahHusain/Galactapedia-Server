from django.db.models.deletion import SET_NULL
from django.db import models


class Asteroid(models.Model):
    stellar_object = models.ForeignKey("Stellar_Object", on_delete=models.CASCADE)