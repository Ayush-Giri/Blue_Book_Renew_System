from django.contrib import admin
from collector.models import CollectorModel, CollectionCenterModel

# Register your models here.
admin.site.register(CollectorModel)
admin.site.register(CollectionCenterModel)