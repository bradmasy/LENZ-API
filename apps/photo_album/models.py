from django.db import models
from django.db.models.query import QuerySet


class PhotoAlbumQuerySet(QuerySet):
    def all(self):
        return self.all()

class PhotoAlbumManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return PhotoAlbumQuerySet(self.model, using=self._db)
    
    def all_albums(self):
        return self.get_queryset().all()
    
class PhotoAlbum(models.Model):
    objects = PhotoAlbumManager()
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)