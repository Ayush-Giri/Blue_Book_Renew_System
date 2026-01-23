from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CollectorModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CollectorModel

User = get_user_model()

@receiver(post_save, sender=User)
def manage_collector_profile(sender, instance, created, **kwargs):
    """
    Automatically creates or deletes a CollectorModel record
    based on the User's is_collector status.
    """
    if instance.is_collector:
        # get_or_create prevents duplicate errors if the profile already exists
        CollectorModel.objects.get_or_create(user=instance)
    else:
        # Optional: If is_collector is unchecked, remove the profile
        CollectorModel.objects.filter(user=instance).delete()


@receiver(post_save, sender=User)
def manage_collector_profile(sender, instance, created, **kwargs):
    if instance.is_collector:
        # get_or_create ensures we don't get an error if it already exists
        CollectorModel.objects.get_or_create(user=instance)
    else:
        # Optional: remove the profile if is_collector is turned off
        CollectorModel.objects.filter(user=instance).delete()