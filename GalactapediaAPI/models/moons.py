from django.db.models.deletion import SET_NULL
from django.db import models


class Moon(models.Model):
    gravity = models.FloatField()
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    stellar_object = models.ForeignKey("Stellar_Object", on_delete=models.CASCADE)
    orbital_period = models.CharField(max_length=25)
