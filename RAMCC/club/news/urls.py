from django.contrib import admin
from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, PostLikeToggle, CommentDelete
from .api import PostLikeAPIToggle, DashboardCounterAPI

app_name = 'news'
urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<slug:slug>', NewsDetail.as_view(), name='post_detail'),
    path('<slug:slug>/<int:id>/delete', CommentDelete.as_view(), name='comment_delete'),
    path('new/', NewsCreate.as_view(), name='post_create'),
    path('<slug:slug>/edit', NewsUpdate.as_view(), name='post_update'),
    path('<slug:slug>/delete', NewsDelete.as_view(), name='post_delete'),
    path('<int:id>/like', PostLikeToggle.as_view(), name='post_like'),

    path('api/<int:id>/like', PostLikeAPIToggle.as_view(), name='post_like_api'),
    path('api/events_count', DashboardCounterAPI.as_view(), name='dashboard_events')
]
