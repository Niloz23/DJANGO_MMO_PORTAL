from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Author(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = RichTextField(verbose_name='Текст')

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    category = models.CharField(max_length=255, choices=[
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ], verbose_name='Категория')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отклик на объявление "{self.ad.title}"'

class Newsletter(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')



