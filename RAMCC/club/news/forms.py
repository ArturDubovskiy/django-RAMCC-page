from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "context",
            "image",
            "draft"
        ]
        widgets = {
            'image': forms.FileInput
        }