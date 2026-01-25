from django.contrib import admin
from renew_request.models import RenewRequest

# Register your models here.

# from django.contrib import admin
# from .models import RenewRequest
#
#
# @admin.register(RenewRequest)
# class RenewRequestAdmin(admin.ModelAdmin):
#     # Show these columns in the list view
#     list_display = ('vehicle', 'user', 'total_amount', 'status', 'request_date')
#
#     # Make total_amount read-only so the user sees the automated calculation
#     readonly_fields = ('total_amount',)
#
#     # Optional: organize the form
#     fields = ('user', 'vehicle', 'insurance', 'service_charge', 'collection_center', 'status', 'total_amount')

# admin.site.register(RenewRequest)


from .models import RenewRequest

@admin.register(RenewRequest)
class RenewRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'total_amount', 'status', 'request_date')
    readonly_fields = ('total_amount',) # User cannot manually edit the calculated total
    fields = ('user', 'vehicle', 'insurance', 'service_charge', 'collection_center', 'status', 'total_amount')
