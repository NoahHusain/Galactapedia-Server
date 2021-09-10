from django.db.models.deletion import SET_NULL
from django.db import models


class Planet(models.Model):
    gravity = models.FloatField()
    star_id = models.ForeignKey("Star", on_delete=models.CASCADE)
    stellar_object_id = models.ForeignKey("stellarobject", on_delete=models.CASCADE)
    orbital_period = models.CharField(max_length=25)
    is_dwarf = models.BooleanField(default= False)
