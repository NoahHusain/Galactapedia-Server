from django.db.models.deletion import SET_NULL
from django.db import models


class Star(models.Model):
    star_type = models.ForeignKey("Star_Type", on_delete=models.CASCADE)
    luminosity = models.FloatField(max_length=10)
    stellar_object = models.ForeignKey("Stellar_Object", on_delete=models.CASCADE)