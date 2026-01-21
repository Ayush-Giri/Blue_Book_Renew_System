from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    """
    extending from AbstractUser to the base user class provided by django
    for basic authentication now we have extended from AsbtractUser class we
    can add our own fields as well in this case we are adding user roles
    """
    # ROLE_CHOICES = (
    #     # the first one is request body and second one is stored in database
    #     ('admin', 'Admin'),
    #     ('collector', 'Collector'),
    #     ('user', 'User'),
    # )
    # role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=30)
    is_collector = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} | {self.email}"
