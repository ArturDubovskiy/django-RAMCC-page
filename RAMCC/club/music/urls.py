from django.urls import path
from .views import CreateAlbum, CreateSong, SongDetail, AlbumDeleteView, MusicHomeView, DeleteSongView

app_name = 'music'

urlpatterns = [
    path('create_album/', CreateAlbum.as_view(), name="create_album"),
    path('<slug:slug>/add_song', CreateSong.as_view(), name="add_song"),
    path('<slug:slug>', SongDetail.as_view(), name="song_detail"),
    path('<slug:slug>/delete', AlbumDeleteView.as_view(), name="album_delete"),
    path('<slug:slug>/delete_song/<int:id>', DeleteSongView.as_view(), name="delete_song"),
    path('', MusicHomeView.as_view(), name="music_home")

]
