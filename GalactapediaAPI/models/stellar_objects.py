from django.db.models.deletion import SET_NULL
from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Stellar_Object(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    mass = models.PositiveBigIntegerField()
    radius = models.BigIntegerField()
    image = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)
    discovered_on = models.DateField(auto_now=False, auto_now_add=False)
    discovered_by = models.CharField(max_length=50)
