from django.db import models

# Create your models here.


class Photo(models.Model):
    """Model for a photo.

    Args:
        models (models): Model for a photo.
    """

    photo = models.ImageField(upload_to="photos/", blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)