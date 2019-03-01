from django import forms
from django.contrib.auth.models import User

from .models import GalleryAlbum, Photo


class GalleryAlbumForm(forms.ModelForm):
    class Meta:
        model = GalleryAlbum
        fields = ['album_title', 'album_logo']


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image_file']
