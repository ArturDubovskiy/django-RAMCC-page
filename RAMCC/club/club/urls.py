from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_auth.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include("music.urls", namespace='music')),
    path('news/', include("news.urls", namespace='news')),
    path('gallery/', include("gallery.urls", namespace='gallery')),
    path('', include("about.urls", namespace='about')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls'))
    # path('adm/', include("dashboard.urls", namespace='dashboard'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



#TODO
#1) Comments profile images out from user_profile_croped_img
#2) Make user_profile
#3) Make password show/hide on login, register form
#4) Make ajax calls for POST methods ar auth, comments ...
#5) Remove inline styles from templates to css files
#6) Oprimize background images load
#7) Normilize image (check for upload MB and sizes)
#8) Fix image not added when edit post
#9) Add not hardcoded status
