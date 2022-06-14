from decimal import Decimal
from urllib import response
from django.test import Client, TestCase
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
        url = '/catalog/book/' + title.replace(" ", "-") + str(date)

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

    
    def test03_details(self):
        "check detail page"
        # get all books
        books = Book.objects.all()
        # get response with all book title
        # check all books
        for book in books:
            response = self.client.get(
                reverse(DETAIL_SERVICE, kwargs={'slug': book.slug}),
                follow=True)
            response_txt = self.decode(response.content)
            self.assertFalse(response_txt.find(book.title) == -1)
            self.assertFalse(response_txt.find(str(book.price)) == -1)
            authors = book.author.all()
            self.assertGreater(len(authors), 0,
                               "number of author must be greater than 0")
            # check authors for this book
            for author in authors:
                self.assertFalse(response_txt.find(author.first_name) == -1)
                self.assertFalse(response_txt.find(author.last_name) == -1)
        # check comments
        comments = Comment.objects.all()
        self.assertEqual(len(comments), self.populate.NUMBERCOMMENTS,
                         "wrong number of comments")
        for comment in comments:
            book = comment.book
            response = self.client.get(reverse(DETAIL_SERVICE,
                                                kwargs={'slug': book.slug}),
                                        follow=True)
            # check comment is in corresponding detail page
            response_txt = self.decode(response.content)
            self.assertFalse(response_txt.find(comment.msg) == -1)