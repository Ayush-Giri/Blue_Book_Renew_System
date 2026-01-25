# from django.contrib.auth import get_user_model
# from django.db import models
# from django.db.models import Q
# from datetime import timedelta, date
# from django.contrib.auth.models import AbstractUser
#
# # Create your models here.
#
#
# # class UserVehicle(models.Model):
# #     brand_and_model = models.CharField(max_length=100)
# #     color = models.CharField(max_length=50)
# #     chassis_number = models.CharField(max_length=100)
# #     engine_number = models.CharField(max_length=100)
# #     issue_data = models.DateField()
# #     expiry_date = models.DateField()
#
#
#
# # class VehicleType(models.Model):
# #     vehicle_type = models.CharField(max_length=50)
#
# User = get_user_model()
#
# class VehicleType(models.Model):
#     """
#     e.g., 'Car/Jeep/Van', 'Two-wheeler', 'Electric Car', 'Tempo'
#     """
#     name = models.CharField(max_length=50, unique=True)
#
#     class Meta:
#         verbose_name = "Vehicle Type"
#         verbose_name_plural = "Vehicle Types"
#
#     def __str__(self):
#         return self.name
#
#
# # class VehicleFuelType(models.Model):
# #     fuel_type = models.CharField(max_length=50)
#
#
# class VehicleFuelType(models.Model):
#     """
#     e.g., 'Petrol/Diesel', 'Electric'
#     """
#     name = models.CharField(max_length=50, unique=True)
#
#     class Meta:
#         verbose_name = "Vehicle Fuel Type"
#         verbose_name_plural = "Vehicle Fuel Types"
#
#     def __str__(self):
#         return self.name
#
#
# # class VehicleCapacity(models.Model):
# #     vehicle_capacity = models.IntegerField()
#
# class VehicleCapacity(models.Model):
#     """
#     MODIFIED: Added a display name and changed field name for clarity.
#     Stores standard capacity points like 125, 150, 1000, 3500 etc.
#     """
#     capacity_value = models.IntegerField()
#
#     def __str__(self):
#         # This makes it readable in the dropdown list
#         return f"{self.capacity_value} CC/kW"
#
#
#     class Meta:
#         verbose_name = "Vehicle Capacity"
#         verbose_name_plural = "Vehicle Capacities"
#
#     def __str__(self):
#         return f"{self.capacity_value}"
#
#
# # class VehicleOwnership(models.Model):
# #     ownership_type = models.CharField()
#
# class VehicleOwnership(models.Model):
#     """
#     e.g., 'Private', 'Public'
#     """
#     name = models.CharField(max_length=50, unique=True)
#
#     class Meta:
#         verbose_name = "Vehicle OwnerShip"
#         verbose_name_plural = "Vehicle Ownerhship's"
#
#     def __str__(self):
#         return self.name
#
#
# class UserVehicle(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
#
#     # Vehicle Identity
#     brand_and_model = models.CharField(max_length=100)  # e.g., "Hyundai Creta"
#     color = models.CharField(max_length=50)
#     chassis_number = models.CharField(max_length=100, unique=True)
#     engine_number = models.CharField(max_length=100, unique=True)
#
#     # Dates
#     issue_date = models.DateField()  # Fixed typo (was issue_data)
#     # Expiry usually calculated from tax payment, but kept as field if manual override needed
#     expiry_date = models.DateField(null=True, blank=True)
#     vehicle_number = models.CharField(max_length=100)
#
#     # Classification (Links to Lookups)
#     vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
#     ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.SET_NULL, null=True)
#     fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.SET_NULL, null=True)
#
#     # Specific Capacity for this vehicle
#     engine_capacity = models.ForeignKey(VehicleCapacity, on_delete=models.SET_NULL, null=True)
#
#     # Stored Calculations
#     current_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#
#     class Meta:
#         verbose_name = "User Vehicle"
#         verbose_name_plural = "User Vehicle's"
#
#     def calculate_tax(self):
#         """
#         Finds the correct tax rule from VehicleTax based on this vehicle's engine capacity.
#         """
#         if not (self.vehicle_type and self.ownership_type and self.fuel_type):
#             return 0
#
#         # Query the Rule Book using the capacity value logic
#         tax_rule = VehicleTax.objects.filter(
#             vehicle_type=self.vehicle_type,
#             ownership_type=self.ownership_type,
#             fuel_type=self.fuel_type,
#             # NEW LOGIC: Look at the capacity_value inside the related VehicleCapacity model
#             # We look for the smallest capacity that is still greater than or equal to our engine_capacity
#             vehicle_capacity__capacity_value__gte=self.engine_capacity
#         ).order_by('vehicle_capacity__capacity_value').first()
#
#         return tax_rule.tax_amount if tax_rule else 0
#
#     def save(self, *args, **kwargs):
#         # Auto-calculate Tax
#         self.current_tax_amount = self.calculate_tax()
#
#         # Auto-set Expiry Date (1 year default)
#         if not self.expiry_date and self.issue_date:
#             try:
#                 self.expiry_date = self.issue_date.replace(year=self.issue_date.year + 1)
#             except ValueError:  # Handle Feb 29 leap year
#                 self.expiry_date = self.issue_date + timedelta(days=365)
#
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.brand_and_model} ({self.engine_capacity}) - {self.user.username}"
#
#     # def __str__(self):
#     #     # Use the related capacity object's value
#     #     cap_label = self.vehicle_capacity.capacity_value if self.vehicle_capacity else "N/A"
#     #     return f"{self.ownership_type} {self.vehicle_type} (Up to {cap_label}): Rs. {self.tax_amount}"
#
#     #         def calculate_tax(self):
#     #             """
#     #             Finds the correct tax rule from VehicleTax based on this vehicle's engine capacity.
#     #             """
#     #             if not (self.vehicle_type and self.ownership_type and self.fuel_type):
#     #                 return 0
#     #
#     #             # Query the Rule Book using the capacity value logic
#     #             tax_rule = VehicleTax.objects.filter(
#     #                 vehicle_type=self.vehicle_type,
#     #                 ownership_type=self.ownership_type,
#     #                 fuel_type=self.fuel_type,
#     #                 # NEW LOGIC: Look at the capacity_value inside the related VehicleCapacity model
#     #                 # We look for the smallest capacity that is still greater than or equal to our engine_capacity
#     #                 vehicle_capacity__capacity_value__gte=self.engine_capacity
#     #             ).order_by('vehicle_capacity__capacity_value').first()
#     #
#     #             return tax_rule.tax_amount if tax_rule else 0
#     #     # """
#     #     # Finds the correct tax rule from VehicleTax based on this vehicle's details.
#     #     # """
#     #     # if not (self.vehicle_type and self.ownership_type and self.fuel_type):
#     #     #     return 0
#     #     #
#     #     # # Query the Rule Book
#     #     # tax_rule = VehicleTax.objects.filter(
#     #     #     vehicle_type=self.vehicle_type,
#     #     #     ownership_type=self.ownership_type,
#     #     #     fuel_type=self.fuel_type,
#     #     #     # Logic: The vehicle capacity must be greater/equal to min...
#     #     #     min_capacity__lte=self.engine_capacity
#     #     # ).filter(
#     #     #     # ...AND (less/equal to max OR max is NULL for 'Above' categories)
#     #     #     Q(max_capacity__gte=self.engine_capacity) | Q(max_capacity__isnull=True)
#     #     # ).first()
#     #     #
#     #     # return tax_rule.tax_amount if tax_rule else 0
#     #
#     # def save(self, *args, **kwargs):
#     #     # 1. Auto-calculate Tax
#     #     self.current_tax_amount = self.calculate_tax()
#     #
#     #     # 2. Auto-set Expiry Date if missing (Default to 1 year from issue for new entries)
#     #     if not self.expiry_date and self.issue_date:
#     #         try:
#     #             # Simple logic: 1 year validity. Adjust as per Nepal fiscal year rules if needed.
#     #             self.expiry_date = self.issue_date.replace(year=self.issue_date.year + 1)
#     #         except ValueError:
#     #             # Handle leap year edge case (Feb 29)
#     #             self.expiry_date = self.issue_date + timedelta(days=365)
#     #
#     #     super().save(*args, **kwargs)
#     #
#     # def __str__(self):
#     #     return f"{self.brand_and_model} - {self.user.username}"
#
#
#
#
#
# # class VehicleTax(models.Model):
# #     pass
#
# # class VehicleTax(models.Model):
# #     """
# #     Stores the tax brackets provided in the government mandate.
# #     Example: Private + Two-wheeler + Petrol + (0 to 125cc) = 2800 NPR
# #     """
# #     # Links to the categories
# #     vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
# #     ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.CASCADE)
# #     fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)
# #
# #     # Capacity Bracket (Decimal used to support both CC and kW)
# #     min_capacity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
# #     max_capacity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
# #     # NOTE: max_capacity is null for "Above X" rules (e.g., Above 3500cc)
# #
# #     # The Tax Amount for this specific bracket
# #     tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
# #     fiscal_year = models.CharField(max_length=20, default="2080/081")
# #
# #     def __str__(self):
# #         range_str = f"{self.min_capacity}-{self.max_capacity if self.max_capacity else 'Above'}"
# #         return f"{self.ownership_type} {self.vehicle_type} ({range_str}): Rs. {self.tax_amount}"
#
#
# class VehicleTax(models.Model):
#     """
#     MODIFIED: Added ForeignKey to VehicleCapacity to link specific brackets.
#     """
#     vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
#     ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.CASCADE)
#     fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)
#
#     # NEW: Direct link to a capacity entry
#     vehicle_capacity = models.ForeignKey(
#         VehicleCapacity,
#         on_delete=models.CASCADE,
#         related_name="tax_rules",
#         null=True, # Set to True initially if you already have data, otherwise False
#         blank=True
#     )
#
#     tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     fiscal_year = models.CharField(max_length=20, default="2080/081")
#
#     class Meta:
#         verbose_name = "Vehicle Tax"
#         verbose_name_plural = "Vehicle Taxes"
#
#     def __str__(self):
#         # Updated string representation to use the linked capacity name
#         cap_label = self.vehicle_capacity if self.vehicle_capacity else f"{self.min_capacity}+"
#         return f"{self.ownership_type} {self.vehicle_type} ({cap_label}): Rs. {self.tax_amount}"
#
#


#### new code #####





from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from datetime import timedelta, date

User = get_user_model()

# --- Lookup Models ---

class VehicleType(models.Model):
    """e.g., 'Car/Jeep/Van', 'Two-wheeler'"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"

    def __str__(self):
        return self.name


class VehicleFuelType(models.Model):
    """e.g., 'Petrol/Diesel', 'Electric'"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Vehicle Fuel Type"
        verbose_name_plural = "Vehicle Fuel Types"

    def __str__(self):
        return self.name


class VehicleCapacity(models.Model):
    """Stores standard capacity points like 125, 1000, 3500 etc."""
    capacity_value = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Vehicle Capacity"
        verbose_name_plural = "Vehicle Capacities"

    def __str__(self):
        return f"{self.capacity_value}"


class VehicleOwnership(models.Model):
    """e.g., 'Private', 'Public'"""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Vehicle Ownership"
        verbose_name_plural = "Vehicle Ownerships"

    def __str__(self):
        return self.name


# --- Tax & User Vehicle Models ---

class VehicleTax(models.Model):
    """Government Tax Rulebook linking categories and capacity to a price."""
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)
    vehicle_capacity = models.ForeignKey(
        VehicleCapacity,
        on_delete=models.CASCADE,
        related_name="tax_rules",
        null=True,
        blank=True
    )
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fiscal_year = models.CharField(max_length=20, default="2080/081")

    class Meta:
        verbose_name = "Vehicle Tax"
        verbose_name_plural = "Vehicle Taxes"

    def __str__(self):
        cap = self.vehicle_capacity.capacity_value if self.vehicle_capacity else "Any"
        return f"{self.ownership_type} {self.vehicle_type} ({cap} CC): Rs. {self.tax_amount}"


class UserVehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")

    # Vehicle Identity
    brand_and_model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    chassis_number = models.CharField(max_length=100, unique=True)
    engine_number = models.CharField(max_length=100, unique=True)
    vehicle_number = models.CharField(max_length=100)

    # Dates
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)

    # Classification (Lookup Links)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    ownership_type = models.ForeignKey(VehicleOwnership, on_delete=models.SET_NULL, null=True)
    fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.SET_NULL, null=True)
    engine_capacity = models.ForeignKey(VehicleCapacity, on_delete=models.SET_NULL, null=True)

    # Calculation Result
    current_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "User Vehicle"
        verbose_name_plural = "User Vehicles"

    def calculate_tax(self):
        """
        Finds the smallest tax bracket that is >= this vehicle's capacity.
        """
        # if not (self.vehicle_type and self.ownership_type and self.fuel_type and self.engine_capacity):
        #     return 0
        #
        # # IMPORTANT: Access the numeric value from the ForeignKey object
        # v_capacity = self.engine_capacity.capacity_value
        #
        # tax_rule = VehicleTax.objects.filter(
        #     vehicle_type=self.vehicle_type,
        #     ownership_type=self.ownership_type,
        #     fuel_type=self.fuel_type,
        #     vehicle_capacity__capacity_value__gte=v_capacity
        # ).order_by('vehicle_capacity__capacity_value').first()
        #
        # return tax_rule.tax_amount if tax_rule else 0


        if not (self.vehicle_type and self.ownership_type and self.fuel_type and self.engine_capacity):
            return 0

            # Convert CharField to integer for a proper numeric comparison
        try:
            current_cap_numeric = int(self.engine_capacity.capacity_value)
        except ValueError:
            return 0

            # Find the tax rule where rule capacity is >= vehicle capacity
        tax_rule = VehicleTax.objects.filter(
            vehicle_type=self.vehicle_type,
            ownership_type=self.ownership_type,
            fuel_type=self.fuel_type
        ).extra(
            where=["CAST(capacity_value AS INTEGER) >= %s"],
            params=[current_cap_numeric]
        ).order_by('vehicle_capacity__capacity_value').first()

        return tax_rule.tax_amount if tax_rule else 0

    def save(self, *args, **kwargs):
        # 1. Update the tax amount before saving
        self.current_tax_amount = self.calculate_tax()

        # 2. Auto-set Expiry Date (1 year default)
        if not self.expiry_date and self.issue_date:
            try:
                self.expiry_date = self.issue_date.replace(year=self.issue_date.year + 1)
            except ValueError:  # Leap year handling (Feb 29)
                self.expiry_date = self.issue_date + timedelta(days=365)

        super().save(*args, **kwargs)

    def __str__(self):
        cap = self.engine_capacity.capacity_value if self.engine_capacity else "N/A"
        return f"{self.brand_and_model} ({cap} CC) - {self.user.username}"