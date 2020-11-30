from django import forms
from users.widgets import CustomClearableFileInput

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "image")
    image = forms.ImageField(
            label="", required=False, widget=CustomClearableFileInput
        )
