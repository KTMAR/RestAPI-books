from django.contrib import admin

from .models import *


class WriterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }




admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(MediaType)
