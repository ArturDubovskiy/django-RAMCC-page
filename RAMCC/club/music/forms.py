from django import forms
from django.contrib.auth.models import User

from .models import MusicAlbum, Song


class AlbumForm(forms.ModelForm):
    class Meta:
        model = MusicAlbum
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']
