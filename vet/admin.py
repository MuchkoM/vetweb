from django.contrib import admin
from . import models

admin.site.register(models.Owner)
admin.site.register(models.Animal)
admin.site.register(models.Species)
admin.site.register(models.Subspecies)
admin.site.register(models.Prevention)
admin.site.register(models.Therapy)
admin.site.register(models.Vaccination)
admin.site.register(models.Diagnosis)
