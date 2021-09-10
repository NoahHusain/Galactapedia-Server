from django.db.models.deletion import SET_NULL
from django.db import models
from django.db import models


class Moon(models.Model):
    gravity = models.FloatField()
    planet_id = models.ForeignKey("Planet", on_delete=models.CASCADE)
    stellar_object_id = models.ForeignKey("stellarobject", on_delete=models.CASCADE)
    orbital_period = models.CharField(max_length=25)
