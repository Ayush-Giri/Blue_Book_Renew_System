from django.db import models
from Blue_Book_Renew_System import settings


class CollectorModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collector_profile'
    )
    collection_center_name = models.CharField(max_length=100)
    collection_center_address = models.CharField(max_length=100)
    collection_center_number = models.CharField(max_length=100)
    is_pickup_available = models.BooleanField()

    def __str__(self):
        return f" collector:{self.user.username} | " \
               f" collection_center: {self.collection_center_name} | " \
               f" collection_center_address: {self.collection_center_address} | " \
               f" collection_center_number: {self.collection_center_number}"

