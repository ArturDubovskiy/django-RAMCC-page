from django.contrib import admin
from news.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ("title", "updated", "created")

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
