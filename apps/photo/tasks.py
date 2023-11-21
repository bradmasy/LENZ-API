from celery import shared_task
from django.utils import timezone
from .models import Photo

@shared_task
def delete_expired_photos():
    expired_photos = Photo.objects.filter(delete_timestamp__lte=timezone.now())
    expired_photos.delete()
