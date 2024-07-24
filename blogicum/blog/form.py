from django import forms

from blog.models import Comment, Post, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author",)
