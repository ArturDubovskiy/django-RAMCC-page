from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, RedirectView
from django.db.models import Q
from django.http import Http404
from .models import GalleryAlbum, Photo
from .forms import GalleryAlbumForm, PhotoForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


class CreateGalleryAlbum(View):

    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = GalleryAlbumForm()
        context = {
            "form": form
        }
        return render(request, 'gallery/create_gallery_album.html', context)

    def post(self, request):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = GalleryAlbumForm(request.POST or None, request.FILES or None)
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
                return render(request, 'gallery/create_gallery_album.html', context)
            album.save()
            return redirect(album.get_absolute_url())
        return render(request, 'gallery/create_gallery_album.html', {"form": form})


class AddPhotos(View):

    def get(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = PhotoForm()
        album = get_object_or_404(GalleryAlbum, slug=slug)
        return render(request, 'gallery/add_photo.html', {"form": form, "album": album})

    def post(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        form = PhotoForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(GalleryAlbum, slug=slug)
        photos = Photo.objects.filter(album=album)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.owner = request.user
            photo.image_file = request.FILES['image_file']
            file_type = photo.image_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'gallery/add_photo.html', context)
            photo.save()
        return redirect(album.get_absolute_url())


class GalleryAlbumView(View):

    def get(self, request, slug):
        if request.user.is_anonymous:
            return render(request, 'permissions.html', status=403)
        user = request.user
        album = get_object_or_404(GalleryAlbum, slug=slug)
        photos = Photo.objects.filter(album=album)
        return render(request, 'gallery/album_detail.html', {'album': album, 'user': user, 'photos': photos})


class GalleryHomeView(View):

    def get(self, request):
        albums = GalleryAlbum.objects.filter(deleted=False)
        return render(request, 'gallery/index.html', {"albums": albums})

