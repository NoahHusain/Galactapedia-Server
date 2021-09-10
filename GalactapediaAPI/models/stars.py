from django.db.models.deletion import SET_NULL
from django.db import models


class Star(models.Model):
    star_type = models.ForeignKey("StarType", on_delete=models.CASCADE)
    luminosity = models.CharField(max_length=50)
    stellar_object = models.ForeignKey("Stellar_Object", on_delete=models.CASCADE)