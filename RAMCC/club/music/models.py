from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import Permission, User
from django.db.models.signals import pre_save
from django.urls import reverse


class MusicAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.CharField(max_length=200, null=True, blank=True)
    album_title = models.CharField(max_length=200, null=False, blank=False)
    genre = models.CharField(max_length=100, null=True, blank=True)
    album_logo = models.FileField(upload_to="albums_logo")
    is_favorite = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title

    def get_absolute_url(self):
        return reverse("music:song_detail", kwargs={"slug": self.slug})

    @property
    def is_deleted(self):
        if (self.deleted):
            return True
        return False


class Song(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(MusicAlbum, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='', upload_to="music/songs")
    is_favorite = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

    @property
    def is_deleted(self):
        if (self.deleted):
            return True
        return False


def create_slug(instance, new_slug=None):
    slug = slugify(instance.album_title)[:20]
    if new_slug is not None:
        slug = new_slug
    qs = MusicAlbum.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_resiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_resiver, sender=MusicAlbum)
