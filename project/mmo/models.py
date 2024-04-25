from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='Postes', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(null=False, default=False)
    is_acept = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.comment_text[:20]}'


class Newsletter(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.code



