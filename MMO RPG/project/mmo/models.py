from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator
import os
from django.conf import settings
class Post(models.Model):
    class CategoryType(models.TextChoices):
        CATEGORY1 = '1', 'Танки'
        CATEGORY2 = '2', 'Хилы'
        CATEGORY3 = '3', 'ДД'
        CATEGORY4 = '4', 'Торговцы'
        CATEGORY5 = '5', 'Гилдмастеры'
        CATEGORY6 = '6', 'Квестгиверы'
        CATEGORY7 = '7', 'Кузнецы'
        CATEGORY8 = '8', 'Кожевники'
        CATEGORY9 = '9', 'Зельевары'
        CATEGORY10 = '10', 'Мастера_заклинаний'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CategoryType.choices, null=False)
    head = models.CharField(max_length=20)
    text = RichTextField(verbose_name='Текст')
    created_at = models.DateTimeField(default=timezone.now)


    def get_author(self):
        author = self.user
        return author

    def __str__(self):
        return f'{self.head}'

    def get_absolute_url(self):
        x = 'posts_detail'
        return reverse(x, args=[str(self.id)])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='Posts', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(null=False, default=False)
    is_acept = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.comment_text[:20]}'

    def get_absolute_url(self):
        x = 'posts_detail'
        return reverse(x, args=[str(self.id)])


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.code

class Photo(models.Model):
    image = models.ImageField(upload_to='photo', blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def photo_url(self):
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.image.url))

    def __str__(self):
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('photos')

class Video(models.Model):
    video = models.FileField(upload_to='video_uploaded', null=True, blank=True, unique=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'avi', 'webm', 'ogv', 'asx'])])
    date_create = models.DateTimeField(auto_now_add=True)

    @property
    def video_url(self):
        return format_html("""
                <video width = "100" height = "100" controls = "controls" poster = "video/duel.jpg">
                <source src = {}>
                video не поддерживается вашим браузером.
                </video>
                """.format(self.video.url))

    def __str__(self):
        return format_html("""
        <video width = "100" height = "100" controls = "controls" poster = "video/duel.jpg">
        <source src = {}>
        video не поддерживается вашим браузером.
        </video>
        """.format(self.video.url))

    def get_absolute_url(self):
        return reverse('video_edit')

class File(models.Model):
    file = models.FileField(upload_to='file_uploaded', null=True, blank=True, unique=True,
                             validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    created_at = models.DateTimeField(auto_now_add=True)

    def read_txt(self):
        name, extension = os.path.splitext(self.file.name)
        if 'txt' in extension:
            path = os.sep.join([settings.MEDIA_ROOT, self.file.name])
            with open(path, 'r') as f:
                lines = f.readlines()
                return lines

    def __str__(self):
        text = self.read_txt()
        return text[0][:10]

class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
