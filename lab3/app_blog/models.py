from django.db import models
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    category = models.CharField('Категорія', max_length=250, help_text='Максимум 250 символів')
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категорія для публікації'
        verbose_name_plural = 'Категорії для публікацій'

    def __str__(self):
        return self.category

class Article(models.Model):
    title = models.CharField('Заголовок', max_length=250, help_text='Максимум 250 символів')
    description = models.TextField('Опис', blank=True)
    pub_date = models.DateTimeField('Дата публікації', default=timezone.now)
    slug = models.SlugField('Слаг', unique_for_date='pub_date')
    main_page = models.BooleanField('Головна', default=False, help_text='Показувати на головній сторінці')
    category = models.ForeignKey(Category, related_name='articles', blank=True, null=True, verbose_name='Категорія', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%m"),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug,
        })

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', verbose_name='Стаття', on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='photos')
    title = models.CharField('Заголовок', max_length=250, blank=True, help_text='Максимум 250 символів')

    class Meta:
        verbose_name = 'Фото для статті'
        verbose_name_plural = 'Фото для статті'

    def __str__(self):
        return self.title
