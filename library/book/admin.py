from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'count']
    list_editable = ['count']

admin.site.register(Book, BookAdmin)