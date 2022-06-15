from django.contrib import admin
from .models import Book
from .models import Author
from .models import Comment

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'price',
                    'number_copies_stock', 'score')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Comment)