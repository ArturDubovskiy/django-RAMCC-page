from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import Permission, User
from django.db.models.signals import pre_save
from django.urls import reverse


class GalleryAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=200, null=False, blank=False)
    album_logo = models.FileField(upload_to="gallery/albums_logo_gallery")
    slug = models.SlugField(unique=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title

    def get_absolute_url(self):
        return reverse("gallery:album_detail", kwargs={"slug": self.slug})

    @property
    def is_deleted(self):
        if (self.deleted):
            return True
        return False


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(default='', upload_to="gallery/photos")
    is_favorite = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.image_file

    @property
    def is_deleted(self):
        if (self.deleted):
            return True
        return False


def create_slug(instance, new_slug=None):
    slug = slugify(instance.album_title)[:20]
    if new_slug is not None:
        slug = new_slug
    qs = GalleryAlbum.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_resiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_resiver, sender=GalleryAlbum)
