from django.db import models
from django.db.models.query import QuerySet


class PhotoAlbumQuerySet(QuerySet):
    """A query set for the PhotoAlbum model.

    Args:
        QuerySet (queryset): A django queryset
    """

    def all_photo_albums(self):
        return self.all()


class PhotoAlbumManager(models.Manager):
    """A manager for the PhotoAlbum model.

    Args:
        models (model): A django model
    """

    def get_queryset(self) -> QuerySet:
        return PhotoAlbumQuerySet(self.model, using=self._db)

    def all_albums(self):
        return self.get_queryset().all_photo_albums()


class PhotoAlbum(models.Model):
    """A model for a photo album, photo albums symbolize a collection of photos for a particular user.

    Args:
        models (model): A django model
    """

    objects = PhotoAlbumManager()
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user_id", "title")
