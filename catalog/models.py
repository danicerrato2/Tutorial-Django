from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timezone
import uuid


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    isbn = models.CharField(
        'ISBN', max_length=13, unique=True,
        help_text='13 Character <a href="https://www.isbn'
        '-international.org/content/what-isbn">ISBN number</a>')
    title = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    path_to_cover_image = models.ImageField(
        upload_to="cover_img")
    number_copies_stock = models.IntegerField()
    date = models.DateField(null=True)
    score = models.DecimalField(decimal_places=2, max_digits=5)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ManyToManyField(Author, 
        help_text='Select an author for this book')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + str(self.date))
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug':self.slug})


class Comment(models.Model):
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    msg = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.book}, by {self.user} on {self.date}'