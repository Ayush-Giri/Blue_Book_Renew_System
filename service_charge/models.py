from django.db import models

# Create your models here.


class ServiceChargeModel(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    fiscal_year = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.amount} | {self.fiscal_year}"


