from django.contrib import admin
from renew_request.models import RenewRequest
from .models import RenewRequest

# Register your models here.


@admin.register(RenewRequest)
class RenewRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'total_amount', 'status', 'request_date')
    readonly_fields = ('total_amount',) # User cannot manually edit the calculated total
    fields = ('user', 'vehicle', 'insurance', 'service_charge', 'collection_center', 'status', 'total_amount')
