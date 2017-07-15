from django.views import generic;
from .models import Album,songs;
from django.views.generic.edit import CreateView,UpdateView,DeleteView;
from django.core.urlresolvers import reverse_lazy,reverse;
from django.shortcuts import render,redirect,get_object_or_404;
from django.contrib.auth import authenticate,login,logout;
from django.views.generic import View;
from .forms import UserForm,SongForm,AlbumForm;
from django.http import JsonResponse;
from django.db.models import Q;
from django.contrib.auth.views import password_reset,password_reset_complete,password_reset_confirm
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']



def reset(request):
    # Wrap the built-in password reset view and pass it the arguments
    # like the template name, email template name, subject template name
    # and the url to redirect after the password reset is initiated.
    return password_reset(request, template_name='music/reset.html',
        email_template_name='music/reset_email.html',
        subject_template_name='music/reset_subject.txt',
        post_reset_redirect=reverse('success'))


def reset_confirm(request, uidb64=None, token=None):
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('success'))


def success(request):
  return render(request, "music/success.html")


class IndexView(generic.ListView):
    template_name = 'music/index.html';

    def get(self,request):
        if not request.user.is_authenticated():
            return render(request,'music/login.html');
        else:
            all_albums= Album.objects.filter(user=request.user);
            song_result=songs.objects.all();
            query=request.GET.get("q");
            if query:
                print("hello")
                all_albums=all_albums.filter(Q(album_title__icontains=query)|
                                             Q(artist__icontains=query)).distinct();
                song_result=song_result.filter(Q(song_title__icontains=query)).distinct();

                return render(request,self.template_name,{'all_albums':all_albums,'songs':song_result})
            else:
                return render(request,self.template_name,{'all_albums':all_albums})


class SongView(View):
    template_name = 'music/songs.html';

    def get(self,request,filter_by):
        if not request.user.is_authenticated():
            return render(request, 'music/login.html')
        else:
            try:
                song_ids = []
                print (request.user.id)
                for album in Album.objects.filter(user=request.user):
                    for song in album.songs_set.all():
                        song_ids.append(song.pk)
                users_songs = songs.objects.filter(pk__in=song_ids)
                if filter_by == 'favorites':
                    users_songs = users_songs.filter(is_favorite=True)
            except Album.DoesNotExist:
                users_songs = []
            return render(request, 'music/songs.html', {
                'song_list': users_songs,
                'filter_by': filter_by,
            })

class create_songs(View):
    form_class = SongForm;
    template_name = 'music/songs_form.html';

    def get(self, request,pk):
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        context = {'album': album,'form': form}
        return render(request, self.template_name, context)

    def post(self, request,pk):
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        if (form.is_valid()):
            albums_songs = album.songs_set.all()

            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, self.template_name, context)
            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, self.template_name, context)

            song.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            'album': album,
            'form': form,
        }
        return render(request, 'music/songs_form.html', context)

class Favorite(View):
    def get(self,request,pk):
        song = get_object_or_404(songs, pk=self.kwargs['pk'])
        try:
            if song.is_favorite:
                song.is_favorite = False
            else:
                song.is_favorite = True
            song.save()
        except (KeyError, songs.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})

class DetailView(generic.DetailView):
    model=Album;
    template_name = 'music/detail.html';

class AlbumCreate(CreateView):
    model=Album;
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
    model=Album;
    fields = ['artist','album_title','genre','album_logo'];

class AlbumDelete(DeleteView):
    model=Album;
    success_url = reverse_lazy('music:index')

class Favorite_Album(View):
    def get(self,request,pk):
        album=get_object_or_404(Album,pk=pk);
        try:
            if album.is_favorite:
                album.is_favorite=False;
            else:
                album.is_favorite=True;
        except(KeyError,Album.DoesNotExist):
            return JsonResponse({'success':False});
        else:
            #print(album.is_favorite)
            return JsonResponse({'success':True});

class UserFormView(View):
    form_class=UserForm;
    template_name='music/registration_form.html';

    def get(self,request):
        form=self.form_class(None);
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST);
        if(form.is_valid()):
            user=form.save(commit=False);

            username=form.cleaned_data['username'];
            password=form.cleaned_data['password'];
            user.set_password(password);
            user.save();

            #return User object if credentials are correct

            user=authenticate(username=username,password=password);
            if user is not None:

                if user.is_active:
                    login(request,user);
                    return redirect('music:index');

        return render(request, self.template_name, {'form': form})

class LoginFormView(View):
    template_name='music/login.html'

    def get(self,request):
        return render(request,self.template_name);

    def post(self,request):
        username=request.POST['username'];
        password=request.POST['password'];
        user=authenticate(username=username,password=password);

        if user is not None:
            if user.is_active:
                login(request,user);
                albums=Album.objects.filter(user=request.user);
                print(albums)
                print("hello in ")
                #return redirect('music:index')
                return render(request,'music/index.html',{'all_albums':albums})
            else:
                return render(request, self.template_name, {'error_message':"Your account hasbeen disabled"})
        else:

            return render(request, self.template_name, {'error_message':"Invalid Login"})

class LogoutFormView(View):
    def get(self,request):
        logout(request);
        return render(request,'music/login.html')

class DeleteSong(DeleteView):
    def post(self,request,pk,song_id):
        album = get_object_or_404(Album, pk=pk)
        song = songs.objects.get(pk=song_id)
        song.delete()
        return render(request, 'music/detail.html', {'album': album})



