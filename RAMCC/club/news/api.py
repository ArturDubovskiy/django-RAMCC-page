from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import get_object_or_404
from news.models import Post
from about.models import JoinClub

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None):
        post = get_object_or_404(Post, id=id)
        url_ = post.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in post.likes.all():
                liked = False
                post.likes.remove(user)
            else:
                liked = True
                post.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)

class DashboardCounterAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        dreaft_count = Post.objects.filter(draft=False).count()
        forms_count = JoinClub.objects.all().count()
        data = {
            "posts": dreaft_count,
            "forms": forms_count
        }
        return Response(data)