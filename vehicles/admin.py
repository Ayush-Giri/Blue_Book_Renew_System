from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.VehicleType)
admin.site.register(models.VehicleFuelType)
admin.site.register(models.VehicleCapacity)
admin.site.register(models.VehicleOwnership)
admin.site.register(models.UserVehicle)
admin.site.register(models.VehicleTax)
