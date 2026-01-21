from django.db import models

# Create your models here.


class InsuranceModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} | {self.price}"

