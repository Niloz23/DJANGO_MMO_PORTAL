from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Post, Comment, OneTimeCode, Photo, Video, File, PostPhoto, PostVideo, PostFile
from mmo.forms import MyActivationCodeForm, CommentForm
from django.contrib.auth import authenticate, login
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from mmo.forms import PostForm, AcceptCommentForm
from .filters import CommentFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin



def activation(request):
    if request.user.is_authenticated:
        return redirect('/posts/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get('code')
                print('code_use',code_use)
                if OneTimeCode.objects.filter(code=code_use):
                    code1 = OneTimeCode.objects.get(code=code_use)
                    p1 = EmailAddress.objects.get(user_id=code1.user.id)
                else:
                    form.add_error(None, 'Неправильный код')
                    return render(request, 'account/email/activate.html', {'form': form})
                if not p1.verified:
                    p1.verified = True
                    p1.save()

                    u1 = User.objects.get(id = p1.user_id)
                    user = authenticate(request, username=u1.username, password=u1.password)
                    if user is not None:
                        login(request, user)

                    code1.delete()
                    return redirect('/accounts/login/')
                else:
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'account/email/activate.html', {'form': form})
            else:
                form.add_error(None, 'Форма не валидна')
                return render(request, 'account/email/activate.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'account/email/activate.html', {'form': form})

class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.request.path_info[7:][:-1]
        c1 = Comment.objects.filter(post_id=post_id)
        context['Postes'] = c1
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = ''

    def form_valid(self, form):
        post = form.save(commit=False)
        author = User.objects.filter(username = self.request.user).values('id')
        author_id = author.values_list('id')[0][0]
        post.user_id = author_id
        post.save()
        photos = self.request.FILES.getlist('photo')
        if photos:
            for photo in photos:
                photo_obj = Photo(image = photo)
                photo_obj.save()
                post_photo_obj = PostPhoto(post=post, photo=photo_obj)
                post_photo_obj.save()

        videos = self.request.FILES.getlist('video')
        if videos:
            for video in videos:
                video_obj = Video(video=video)
                video_obj.save()
                post_video_obj = PostVideo(post=post, video=video_obj)
                post_video_obj.save()

        files = self.request.FILES.getlist('file')
        if files:
            for file in files:
                file_obj = File(file=file)
                file_obj.save()
                post_file_obj = PostFile(post=post, file=file_obj)
                post_file_obj.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def test_func(self):
        news = self.get_object()
        return news.user == self.request.user

class PostDelete(LoginRequiredMixin,UserPassesTestMixin,  DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def test_func(self):
        news = self.get_object()
        return news.user == self.request.user

class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    success_url = reverse_lazy('posts_list')

class CommentAccept(LoginRequiredMixin, UpdateView):
    form_class = AcceptCommentForm
    model = Comment
    queryset = Comment.objects.filter(is_acept=False)
    template_name = 'comment_accept.html'
    success_url = '/comments/'

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = '/comments/'

class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    ordering = '-created_at'
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 5

    def get_queryset(self):
        #queryset = super().get_queryset()
        u1 = self.request.user
        c1 = Comment.objects.select_related('post').filter(post__user=u1)
        queryset = c1
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u1 = self.request.user
        print('self.request.user',self.request.user)
        c1 = Comment.objects.select_related('post').filter(post__user=u1)
        context['filterset'] = self.filterset
        return context

class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photos.html'
    context_object_name = 'photos'
    paginate_by = 10

