from django import forms
from django.contrib.auth import get_user_model

from blog.models import Post


class PostForm(forms.ModelForm):
    """ for showing and change posts """

    class Meta:
        model = Post
        fields = ['title', 'text']
        read_only_fields = ['author', 'date_created', 'date_updated']


class UserForm(forms.ModelForm):

    """ For showing User """

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        read_only_fields = ['id', 'username']