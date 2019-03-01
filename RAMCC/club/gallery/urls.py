from django.urls import path
from .views import CreateGalleryAlbum, AddPhotos, GalleryAlbumView, GalleryHomeView

app_name = 'gallery'

urlpatterns = [
    path('create_gallery/', CreateGalleryAlbum.as_view(), name="create_gallery_album"),
    path('<slug:slug>/add_photos', AddPhotos.as_view(), name="add_photos"),
    path('<slug:slug>', GalleryAlbumView.as_view(), name="album_detail"),
    path('', GalleryHomeView.as_view(), name="gallery_home")

]
