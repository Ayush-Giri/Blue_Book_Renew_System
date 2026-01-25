from django.db import models
from vehicles.models import UserVehicle
from django.contrib.auth import get_user_model
from insurance.models import InsuranceModel
from service_charge.models import ServiceChargeModel
from collector.models import CollectorModel

User = get_user_model()

# Create your models here.

class RenewRequest(models.Model):
    # Status choices to track the lifecycle of the request
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="renew_requests"
    )

    # Linked Models
    vehicle = models.ForeignKey(
        UserVehicle,
        on_delete=models.PROTECT,
        related_name="renewals"
    )
    insurance = models.ForeignKey(
        InsuranceModel,
        on_delete=models.PROTECT
    )
    service_charge = models.ForeignKey(
        ServiceChargeModel,
        on_delete=models.PROTECT
    )
    collection_center = models.ForeignKey(
        CollectorModel,
        on_delete=models.SET_NULL,
        null=True
    )

    # Tracking Fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Sum of Tax + Insurance + Service Charge"
    )
    request_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Renew Request"
        verbose_name_plural = "Renew Requests"

    # def save(self, *args, **kwargs):
    #     # # Automatically calculate total amount if not set
    #     # # Total = Vehicle Tax + Insurance Price + Service Charge Amount
    #     # if not self.total_amount:
    #     #     tax = self.vehicle.current_tax_amount or 0
    #     #     ins = self.insurance.price or 0
    #     #     serv = self.service_charge.amount or 0
    #     #     self.total_amount = tax + ins + serv
    #     # super().save(*args, **kwargs)
    #         # 1. Fetch the tax from the vehicle table
    #         # 2. Fetch insurance price
    #         # 3. Fetch service charge
    #
    #     tax = self.vehicle.current_tax_amount or 0
    #     ins = self.insurance.price or 0
    #     serv = self.service_charge.amount or 0
    #
    #     # Calculate Total: Sum of Tax + Insurance + Service Charge
    #     self.total_amount = tax + ins + serv

        # super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # 1. Fetch current tax directly from the vehicle's calculation logic
        # This ensures even if the vehicle table didn't save the tax, we find it now
        tax = 0
        if self.vehicle:
            # If current_tax_amount is empty, trigger the calculation manually
            tax = self.vehicle.current_tax_amount or self.vehicle.calculate_tax()

        # 2. Fetch prices from related models
        ins = self.insurance.price if self.insurance else 0
        serv = self.service_charge.amount if self.service_charge else 0

        # 3. Calculate and set the total
        self.total_amount = tax + ins + serv

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Renewal for {self.vehicle.vehicle_number} - {self.status}"

