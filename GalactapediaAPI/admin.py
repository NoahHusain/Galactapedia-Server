from django.contrib import admin
from GalactapediaAPI.models import Stellar_Object, Star, Planet, Moon, Star_Type, Asteroid

# Register your models here.

admin.site.register(Star)
admin.site.register(Stellar_Object)
admin.site.register(Planet)
admin.site.register(Moon)
admin.site.register(Star_Type)
admin.site.register(Asteroid)
