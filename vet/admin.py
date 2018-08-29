from django.contrib import admin
from . import models

admin.site.register(models.Owner)
admin.site.register(models.Animal)
admin.site.register(models.Appointment)
admin.site.register(models.Species)
admin.site.register(models.Subspecies)
