from django import forms

from .models import Comments, User, Post


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

