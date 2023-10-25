from django.db import models
from apps.photo_album.models import PhotoAlbum


class JourneyQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def all_journeys(self):
        return self.all()


class JourneyManager(models.Manager):
    def get_queryset(self):
        return JourneyQuerySet(self.model, using=self._db)

    def get_all_journeys(self):
        return self.get_queryset().all_journeys()

    def get_active_journeys(self):
        return self.get_queryset().active()


class Journey(models.Model):
    """Represents a journey. A journey is a collection of photo albums that are related to a life journey
    ie. going to university, getting married, career, big trips etc.

    Args:
        models (model): Django Model
    """

    choices = (("SMALL", "S"), ("MEDIUM", "M"), ("LARGE", "L"))
    objects = JourneyManager()
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=100, choices=choices, default="S")

    class Meta:
        unique_together = ("title", "user_id")


class PhotoAlbumJourney(models.Model):
    """Represents the relationship between a photo album and a journey.

    Args:
        models (Model): Django Model
    """

    id = models.AutoField(primary_key=True)
    journey_id = models.ForeignKey("journey.Journey", on_delete=models.CASCADE)
    photo_album_id = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("journey_id", "photo_album_id")
