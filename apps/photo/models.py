from django.db import models
from django.db.models.query import QuerySet

# Create your models here.


class PhotoQuerySet(QuerySet):
    def if_active(self):
        return self.filter(active=True)

    def by_id(self, id):
        return self.filter(id=id)


class PhotoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return PhotoQuerySet(self.model, using=self._db)

    def if_active(self):
        return self.get_queryset().if_active()

    def by_tags(self, tags):
        pass

    def by_id(self, id):
        return self.get_queryset().by_id(id)


class Photo(models.Model):
    """Model for a photo.

    Args:
        models (models): Model for a photo.
    """

    objects = PhotoManager()
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    photo = models.BinaryField(blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class PhotoAlbumPhoto(models.Model):
    id = models.AutoField(primary_key=True)
    photo_album_id = models.ForeignKey(
        "photo_album.PhotoAlbum", on_delete=models.CASCADE
    )
    photo_id = models.ForeignKey("Photo", on_delete=models.CASCADE)

    unique_together = ("photo_album_id", "photo_id")
