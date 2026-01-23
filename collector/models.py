from django.db import models
from Blue_Book_Renew_System import settings


class CollectionCenterModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    is_pickup_available = models.BooleanField()

    def __str__(self):
        return f"{self.name} | {self.address} | {self.is_pickup_available}"


class CollectorModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collector_profile'
    )
    collection_center = models.OneToOneField(
        CollectionCenterModel,
        on_delete=models.CASCADE,
        related_name='manager',
        null=True,
        blank=True

    )

    def __str__(self):
        return f" collector:{self.user.username} | " \
               # f" collection_center: {self.collection_center.name} | " \
               # f" collection_center_address: {self.collection_center.address} | " \
               # f" collection_center_number: {self.collection_center.phone_number}"



