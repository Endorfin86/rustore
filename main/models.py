from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Groups(models.Model):
    slug = models.SlugField('Уникальный URL', unique=True)
    title = models.CharField('Имя', max_length=100)
    desc = models.TextField('Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class Apps(models.Model):
    slug = models.SlugField('Уникальный URL', unique=True)
    title = models.CharField('Название приложения', max_length=100)
    desc = models.TextField('Описание')
    image = models.ImageField('Иконка приложения', default='default.png', upload_to='apps_images')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Группа приложения')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app', kwargs={'slug': self.group.slug, 'slug_app': self.slug})
    

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

class Comment(models.Model):
    text = RichTextUploadingField(verbose_name='Комментарий')
    avtor = models.ForeignKey(User, default='user', verbose_name='Автор', on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, default='app', verbose_name='Приложение', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return f'В {self.app} написал {self.avtor}'

