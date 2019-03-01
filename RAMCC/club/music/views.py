from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, RedirectView
from .forms import AlbumForm, SongForm
from .models import MusicAlbum, Song
from django.db.models import Q
from django.http import Http404

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class CreateAlbum(View):

    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = AlbumForm()
        context = {
            "form": form
        }
        return render(request, 'music/create_album.html', context)

    def post(self, request):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            if album.artist == None:
                album.artist = "Mixed"
            album.save()
            return render(request, 'music/detail.html', {"album": album})
        return render(request, 'music/create_album.html', {"form": form})


class CreateSong(View):

    def get(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = SongForm()
        album = get_object_or_404(MusicAlbum, slug=slug)
        return render(request, 'music/add_song.html', {"form": form, "album": album})

    def post(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(MusicAlbum, slug=slug)
        if form.is_valid():
            album_songs = album.song_set.all()
            for song in album_songs:
                if song.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/add_song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.owner = request.user
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/add_song.html', context)
            song.save()
        return render(request, 'music/detail.html', {'album': album})


class SongDetail(View):

    def get(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        user = request.user
        album = get_object_or_404(MusicAlbum, slug=slug)
        return render(request, 'music/detail.html', {'album': album, 'user': user})


class AlbumDeleteView(View):

    def post(self, request, slug):
        if request.user.is_staff:
            album = get_object_or_404(MusicAlbum, slug=slug)
            album.deleted = True
            album.save()
            albums = MusicAlbum.objects.filter(deleted=False)
            return render(request, 'music/music_index.html', {"albums": albums})
        raise Http404

class MusicHomeView(View):

    def get(self, request):
        albums = MusicAlbum.objects.filter(deleted=False)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/music_index.html', {"albums": albums,
                                                              "songs": song_results})
        else:
            return render(request, 'music/music_index.html', {"albums": albums})


class DeleteSongView(View):

        def post(self, request, slug, id):
            if request.user.is_anonymous:
                raise Http404
            album = get_object_or_404(MusicAlbum, slug=slug)
            song = get_object_or_404(Song, pk=id)
            song.delete()
            return redirect(album.get_absolute_url())

    