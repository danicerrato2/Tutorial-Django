from django.contrib import admin
from .models import Book
from .models import Author
from .models import Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    fields = ['first_name', 'last_name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'price',
                    'number_copies_stock', 'score')