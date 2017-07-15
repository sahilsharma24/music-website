from django.conf.urls import url;
from . import views;

app_name='music';

urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'register/$', views.UserFormView.as_view(), name='register'),

    #login_user
    url(r'login_user/$',views.LoginFormView.as_view(),name='login_user'),

    #logout_user
    url(r'logout_user/$',views.LogoutFormView.as_view(),name='logout_user'),

    # /music/712/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/favorite
    url(r'^(?P<pk>[0-9]+)/favorite/$', views.Favorite.as_view(), name='favorite'),

    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.SongView.as_view(), name='songs'),

    url(r'^(?P<pk>[0-9]+)/create_song/$', views.create_songs.as_view(), name='create_song'),

    url(r'^(?P<pk>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.DeleteSong.as_view(), name='delete_song'),

    url(r'^(?P<pk>[0-9]+)/favorite_album/$', views.Favorite_Album.as_view(), name='favorite_album'),


    #/music/album/add/
    url(r'album/add/$',views.AlbumCreate.as_view(),name='album-add'),

    #/music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name='album-update'),

#/music/album/2/
    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),

]