from django.contrib.auth.models import User;
from django import forms;
from .models import Album,songs

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput);
    class Meta:
        model=User;
        fields=['username','email','password'];

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = songs
        fields = ['song_title', 'audio_file']