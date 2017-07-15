from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import password_reset_confirm,password_reset,password_reset_done,password_reset_complete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
url(r'password_reset$', 'music.views.reset', name='password_reset'),
    url(r'success','music.views.success',name='success'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'music.views.reset_confirm', name='password_reset_confirm'),
    #url(r'password_reset/done$', password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='password_reset_confirm'),
    #url(r'password_reset/complete',password_reset_complete,name='password_reset_complete'),
    url(r'^music/',include('music.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

