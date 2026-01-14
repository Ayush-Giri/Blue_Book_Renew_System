from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from datetime import timedelta, date
from django.contrib.auth.models import AbstractUser

# Create your models here.


# class UserVehicle(models.Model):
#     brand_and_model = models.CharField(max_length=100)
#     color = models.CharField(max_length=50)
#     chassis_number = models.CharField(max_length=100)
#     engine_number = models.CharField(max_length=100)
#     issue_data = models.DateField()
#     expiry_date = models.DateField()



# class VehicleType(models.Model):
#     vehicle_type = models.CharField(max_length=50)

User = get_user_model()

class VehicleType(models.Model):
    """
    e.g., 'Car/Jeep/Van', 'Two-wheeler', 'Electric Car', 'Tempo'
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# class VehicleFuelType(models.Model):
#     fuel_type = models.CharField(max_length=50)


class VehicleFuelType(models.Model):
    """
    e.g., 'Petrol/Diesel', 'Electric'
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# class VehicleCapacity(models.Model):
#     vehicle_capacity = models.IntegerField()

class VehicleCapacity(models.Model):
    """
    MODIFIED: Added a display name and changed field name for clarity.
    Stores standard capacity points like 125, 150, 1000, 3500 etc.
    """
    capacity_value = models.IntegerField(help_text="CC for fuel or kW for electric")

    def __str__(self):
        return f"{self.capacity_value}"


# class VehicleOwnership(models.Model):
#     ownership_type = models.CharField()

class VehicleOwnership(models.Model):
    """
    e.g., 'Private', 'Public'
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserVehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")

    # Vehicle Identity
    brand_and_model = models.CharField(max_length=100)  # e.g., "Hyundai Creta"
    color = models.CharField(max_length=50)
    chassis_number = models.CharField(max_length=100, unique=True)
    engine_number = models.CharField(max_length=100, unique=True)

    # Dates
    issue_date = models.DateField()  # Fixed typo (was issue_data)
    # Expiry usually calculated from tax payment, but kept as field if manual override needed
    expiry_date = models.DateField(null=True, blank=True)

    # Classification (Links to Lookups)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.SET_NULL, null=True)
    fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.SET_NULL, null=True)

    # Specific Capacity for this vehicle
    engine_capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="CC for fuel, kW for electric")

    # Stored Calculations
    current_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_tax(self):
        """
        Finds the correct tax rule from VehicleTax based on this vehicle's details.
        """
        if not (self.vehicle_type and self.ownership_type and self.fuel_type):
            return 0

        # Query the Rule Book
        tax_rule = VehicleTax.objects.filter(
            vehicle_type=self.vehicle_type,
            ownership_type=self.ownership_type,
            fuel_type=self.fuel_type,
            # Logic: The vehicle capacity must be greater/equal to min...
            min_capacity__lte=self.engine_capacity
        ).filter(
            # ...AND (less/equal to max OR max is NULL for 'Above' categories)
            Q(max_capacity__gte=self.engine_capacity) | Q(max_capacity__isnull=True)
        ).first()

        return tax_rule.tax_amount if tax_rule else 0

    def save(self, *args, **kwargs):
        # 1. Auto-calculate Tax
        self.current_tax_amount = self.calculate_tax()

        # 2. Auto-set Expiry Date if missing (Default to 1 year from issue for new entries)
        if not self.expiry_date and self.issue_date:
            try:
                # Simple logic: 1 year validity. Adjust as per Nepal fiscal year rules if needed.
                self.expiry_date = self.issue_date.replace(year=self.issue_date.year + 1)
            except ValueError:
                # Handle leap year edge case (Feb 29)
                self.expiry_date = self.issue_date + timedelta(days=365)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand_and_model} - {self.user.username}"





# class VehicleTax(models.Model):
#     pass

# class VehicleTax(models.Model):
#     """
#     Stores the tax brackets provided in the government mandate.
#     Example: Private + Two-wheeler + Petrol + (0 to 125cc) = 2800 NPR
#     """
#     # Links to the categories
#     vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
#     ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.CASCADE)
#     fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)
#
#     # Capacity Bracket (Decimal used to support both CC and kW)
#     min_capacity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     max_capacity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     # NOTE: max_capacity is null for "Above X" rules (e.g., Above 3500cc)
#
#     # The Tax Amount for this specific bracket
#     tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     fiscal_year = models.CharField(max_length=20, default="2080/081")
#
#     def __str__(self):
#         range_str = f"{self.min_capacity}-{self.max_capacity if self.max_capacity else 'Above'}"
#         return f"{self.ownership_type} {self.vehicle_type} ({range_str}): Rs. {self.tax_amount}"


class VehicleTax(models.Model):
    """
    MODIFIED: Added ForeignKey to VehicleCapacity to link specific brackets.
    """
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)

    # NEW: Direct link to a capacity entry
    vehicle_capacity = models.ForeignKey(
        VehicleCapacity,
        on_delete=models.CASCADE,
        related_name="tax_rules",
        null=True, # Set to True initially if you already have data, otherwise False
        blank=True
    )

    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fiscal_year = models.CharField(max_length=20, default="2080/081")

    def __str__(self):
        # Updated string representation to use the linked capacity name
        cap_label = self.vehicle_capacity if self.vehicle_capacity else f"{self.min_capacity}+"
        return f"{self.ownership_type} {self.vehicle_type} ({cap_label}): Rs. {self.tax_amount}"


