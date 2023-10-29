from django.db import models
from django.db.models.query import QuerySet


# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class PhotoQuerySet(QuerySet):
    def if_active(self):
        return self.filter(active=True)

    def by_id(self, id):
        return self.filter(id=id)

    def by_tag(self, tags):
        return self.filter(tags in tags)

    def get_photo_count(self):
        return self.all().count()

    def search_queryset(self, query: dict):
        from_date = query.get("from_date")
        to_date = query.get("to_date")

        return (
            self.filter(title__iregex=f"{query.get('title')}")
            .filter(description__iregex=f"{query.get('description')}")
            .filter(created_at__range=(from_date, to_date))
        )


class PhotoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return PhotoQuerySet(self.model, using=self._db)

    def if_active(self):
        return self.get_queryset().if_active()

    def by_tags(self, tags):
        pass

    def by_id(self, id):
        return self.get_queryset().by_id(id)

    def by_search_query(self, query):
        return self.get_queryset().search_queryset(query)


class Photo(models.Model):
    """Model for a photo.

    Args:
        models (models): Model for a photo.
    """

    objects = PhotoManager()
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    photo = models.BinaryField(blank=False, null=False)
    tags = models.ManyToManyField(Tag)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, blank=False, null=False)


class PhotoAlbumPhotoQuerySet(QuerySet):
    def if_active(self):
        return self.filter(active=True)

    def by_album_id(self, id):
        return self.filter(photo_album_id=id)

    def by_id(self, id):
        return self.filter(id=id)


class PhotoAlbumPhotoManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return PhotoAlbumPhotoQuerySet(self.model, using=self._db)

    def get_by_album_id(self, id):
        return self.get_queryset().by_album_id(id)


class PhotoAlbumPhoto(models.Model):
    objects = PhotoAlbumPhotoManager()
    id = models.AutoField(primary_key=True)
    photo_album_id = models.ForeignKey(
        "photo_album.PhotoAlbum", on_delete=models.CASCADE
    )
    photo_id = models.ForeignKey("Photo", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("photo_album_id", "photo_id")
