from django_resized import ResizedImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)


def imageUploader(instance, filename):
    return '/'.join(['images', str(instance.name), filename])


class Writer(models.Model):
    """Писатель"""

    name = models.CharField(max_length=255, verbose_name='Писатель')
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    slug = models.SlugField()
    image = ResizedImageField(size=[500, 300], upload_to=imageUploader, blank=True, null=True)

    # image = models.ImageField(upload_to=imageUploader, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Писатель'
        verbose_name_plural = 'Писатели'


class MediaType(models.Model):
    """Формат носителя"""

    name = models.CharField(max_length=100, verbose_name='Тип носителя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип носителя'
        verbose_name_plural = 'Тип носителей'


class Genre(models.Model):
    """Жанр книги"""

    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):
    """Книга"""

    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, verbose_name='Писатель', null=True)
    name = models.CharField(max_length=255, verbose_name='Название книги')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    media_type = models.ForeignKey(MediaType, verbose_name='Носитель', on_delete=models.CASCADE, null=True)
    release_date = models.DateField(verbose_name='Дата релиза', null=True)
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    stock = models.IntegerField(default=1, verbose_name='Наличие')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Предолжение недели?')
    image = ResizedImageField(size=[1920, 1080], upload_to=imageUploader, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owner_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='reader_books')

    def __str__(self):
        return f'{self.id} | {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)

    def ct_model(self):
        return self._meta.model_name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = 'Книги'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'BAD'),
        (2, 'NOT BAD'),
        (3, 'GOOD'),
        (4, 'NICE'),
        (5, 'AMAZING')

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username} | {self.book.name} | like: {self.like} | in_bookmarks: {self.in_bookmarks}' \
               f' | rating: {self.rating}'
