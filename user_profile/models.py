from django.db import models
from accounts.models import User
from django.conf import settings
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    """
    Profile model linked 1-to-1 with User
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    image = models.ImageField(upload_to="media/", null=True, blank=True)
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    member_since = models.DateField()

    def __str__(self):
        return self.name
