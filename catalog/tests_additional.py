from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .management.commands.populate import Command

###################
# You may modify the following variables
from .models import Author as Author, Comment
from .models import Book as Book

DETAIL_SERVICE = "book-detail"
SEARCH_SERVICE = "search"
SEARCH_TITLE = "Search"

SERVICE_DEF = {DETAIL_SERVICE: {
        "title": "",
    },
    SEARCH_SERVICE: {
        "title": SEARCH_TITLE,
    },
}
# PLease do not modify anything below this line
###################


class ServiceBaseTest(TestCase):
    def setUp(self):
        self.populate = Command()
        self.populate.handle()

    def tearDown(self):
        self.populate.cleanDataBase()

    @classmethod
    def decode(cls, txt):
        return txt.decode("utf-8")


class CatalogAdditionalTests(ServiceBaseTest):
    authorDict = {
        "first_name": 'Pedro',
        "last_name": 'Picapiedra',
    }
    bookDict = {
        "isbn": '1234567890123',
        "title": 'title_1',
        "price": Decimal(23.32),
        "path_to_cover_image": 'kk.jpg',
        "number_copies_stock": 23,
        "score": 9,
        "date":"2000-02-20",
    }
    userDict = {
        "username": 'pmarmol',
        "password": 'troncomovil',
        "first_name": 'Pablo',
        "last_name": 'Marmol',
        "email": 'p.marmol@cantera.com',
    }

    def create_check(self, dictionary, ObjectClass):
        """ create an object of the class 'ObjectClass'
        using the dictionary. Then,
        check that all key-values in the
        dictionary are attributes in the object.
        return created object of class Object
        """
        # check that str function exists
        self.assertTrue(ObjectClass.__str__ is not object.__str__)
        # create object
        item = ObjectClass.objects.create(**dictionary)
        for key, value in dictionary.items():
            self.assertEqual(getattr(item, key), value)
        # execute __str__() so all the code in models.py is checked
        item.__str__()
        return item

    def test01_book_url(self):
        book = self.create_check(self.bookDict, Book)
        author = self.create_check(self.authorDict, Author)
        book.author.add(author)
        book.save()

        title = book.title
        date = book.date
        url = '/home/book/' + title.replace(" ", "-") + str(date)

        self.assertEqual(book.get_absolute_url(), url)

    def test02_lists_in_homepage(self):
        top5_score = Book.objects.all().order_by('-score')[:5]
        last5 = Book.objects.all().order_by('-date')[:5]

        response = self.client.get(
            reverse("home", kwargs={}), follow=True)
        response_text = self.decode(response.content)

        for book in top5_score:
            self.assertTrue(response_text.find(book.title) != -1)

        for book in last5:
            self.assertTrue(response_text.find(book.title) != -1)