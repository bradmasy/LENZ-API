from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Photo


@receiver(pre_delete, sender=Photo)
def set_delete_timer(sender, instance, **kwargs):
    instance.delete_timestamp = timezone.now() + timezone.timedelta(days=31)
    instance.save()
