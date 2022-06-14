# Populate database
# This file has to be placed within the
# catalog/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate
#
# use module Faker generator to generate data (https://zetcode.com/python/faker/)

import os

from django.core.management.base import BaseCommand
from django.template.defaultfilters import random, slugify
import pytz
from catalog.models import (Author, Book, Comment)
from django.contrib.auth.models import User
from faker import Faker
# define STATIC_PATH in settings.py
from bookshop.settings import STATIC_PATH
from PIL import Image, ImageDraw, ImageFont
import random

FONTDIR = "/usr/share/fonts/truetype/freauthort properly"
#


class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate database
           """

    # def add_arguments(self, parser):

    # handle is another compulsory name, do not change it"
    # handle function will be executed by 'manage populate'
    def handle(self, *args, **kwargs):
        # check a variable that is unlikely been set out of heroku
        # as DYNO to decide which font directory should be used.
        # Be aware that your available fonts may be different
        # from the ones defined here
        if 'DYNO' in os.environ:
            self.font = \
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
        else:
            self.font = \
                "/usr/share/fonts/truetype/freefont/FreeMono.ttf"


        self.NUMBERUSERS = 20
        self.NUMBERBOOKS = 30
        self.NUMBERAUTHORS = 6
        self.MAXAUTHORSPERBOOK = 3
        self.NUMBERCOMMENTS = self.NUMBERBOOKS * 5
        self.MAXCOPIESSTOCK = 30
        self.cleanDataBase()   # clean database
        # The faker.Faker() creates and initializes a faker generator,
        self.faker = Faker()
        self.user()
        self.author()
        self.book()
        self.comment()
        # check a variable that is unlikely been set out of heroku
        # as DYNO to decide which font directory should be used.
        # Be aware that your available fonts may be different 
        # from the ones defined here 

    def cleanDataBase(self):
        # delete all models stored (clean table)
        # in database
        User.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        Comment.objects.all().delete()

        User.objects.create_superuser('alumnodb', 'alumnodb@gmail.com', 'alumnodb')

    def user(self):
        " Insert users"
        for i in range(self.NUMBERUSERS):
           User.objects.create_user(username=self.faker.user_name(),
                       password=self.faker.password(),
                       first_name=self.faker.first_name(),
                       last_name=self.faker.last_name(),
                       email=self.faker.email())

    def author(self):
        " Insert authors"
        for i in range(self.NUMBERAUTHORS):
           author = Author(first_name=self.faker.first_name(),
                           last_name=self.faker.last_name())
           author.save() 

    def cover(self, book):
        """create fake cover image.
           This function creates a very basic cover
           that show (partially),
           the primary key, title and author name"""

        img = Image.new('RGB', (200, 300), color=(73, 109, 137))
        # your font directory may be different
        fnt = ImageFont.truetype(
            self.font,
            28, encoding="unic")
        d = ImageDraw.Draw(img)
        d.text((10, 100), "PK %05d" % int(book.id), font=fnt, fill=(255, 255, 0))
        d.text((20, 150), book.title[:15], font=fnt, fill=(255, 255, 0))
        d.text((20, 200), "By %s" % str(
            book.author.all()[0])[:15], font=fnt, fill=(255, 255, 0))
        img.save(os.path.join(
            STATIC_PATH + 'covers/', str(book.path_to_cover_image)))

    def book(self):
        " Insert books"
        for i in range(self.NUMBERBOOKS):
            book = Book(isbn=str(self.faker.random_number(digits=13, fix_len=True)),
                       title=self.faker.sentence(),
                       price=self.faker.random_number(digits=2, fix_len=False),
                       number_copies_stock=self.faker.random_number(digits=2, fix_len=False),
                       score=self.faker.pydecimal(left_digits=1, right_digits=2, positive=True),
                       date=self.faker.date())
            book.save()
            book.slug = slugify(book.title + str(book.date))
            book.path_to_cover_image=str(book.id) + '.jpg'
            book.save()
            for i in range(self.MAXAUTHORSPERBOOK):
                book.author.add(Author.objects.all()[random.randint(0, self.NUMBERAUTHORS - 1)])
            book.save()
            self.cover(book)
             

    def comment(self):
        " Insert comments"
        for i in range(self.NUMBERCOMMENTS):
            comment = Comment(date=self.faker.date_time(tzinfo=pytz.UTC),
                              msg=self.faker.paragraph())
            comment.book = Book.objects.all()[random.randint(0, self.NUMBERAUTHORS - 1)]
            comment.user = User.objects.all()[random.randint(0, self.NUMBERAUTHORS - 1)]
            comment.save()
