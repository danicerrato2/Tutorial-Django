from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .management.commands.populate import Command
from django.contrib.auth.models import User

###################
# You may modify the following variables
from .models import Author
from .models import Book
from .models import Vote

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

    bookDict = {
        "isbn": '1234567890123',
        "title": 'title_1',
        "price": Decimal(23.32),
        "path_to_cover_image": 'kk.jpg',
        "number_copies_stock": 23,
        "score": None,
        "num_votes": 0,
        "date":"2000-02-20",
    }
    user1Dict = {
        "username": 'dcerrato',
        "password": 'password',
        "first_name": 'Daniel',
        "last_name": 'Cerrato',
        "email": 'd.cerrato@correo.com',
    }
    user2Dict = {
        "username": 'ahsoka_tano',
        "password": 'soypadawan',
        "first_name": 'Ahsoka',
        "last_name": 'Tano',
        "email": 'a.tano@correo.es',
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

    def test01_different_users_voting(self):
        book = self.create_check(self.bookDict, Book)
        user1 = self.create_check(self.user1Dict, User)
        user2 = self.create_check(self.user2Dict, User)

        # Comprobamos score y numero de votos iniciales
        self.assertEqual(book.score, None)
        self.assertEqual(book.num_votes, 0)

        # Creamos el voto del primer usuario
        vote1 = Vote(score=10, book=book, user=user1)
        vote1.save()

        # Comprobamos que se ha actualizado el score y los votos
        self.assertEqual(book.score, 10)
        self.assertEqual(book.num_votes, 1)

        # Creamos el voto del segundo usuario
        vote2 = Vote(score=0, book=book, user=user2)
        vote2.save()

        # Comprobamos que el score es la media de ambas votaciones
        self.assertEqual(book.score, 5)
        self.assertEqual(book.num_votes, 2)
        

    def test02_same_user_voting(self):
        book = self.create_check(self.bookDict, Book)
        user1 = self.create_check(self.user1Dict, User)

        # Comprobamos score y numero de votos iniciales
        self.assertEqual(book.score, None)
        self.assertEqual(book.num_votes, 0)

        # Creamos el primer voto del unico usuario
        vote1 = Vote(score=10, book=book, user=user1)
        vote1.save()

        # Comprobamos que se ha actualizado el score y los votos
        self.assertEqual(book.score, 10)
        self.assertEqual(book.num_votes, 1)

        # Creamos el primer voto del unico usuario
        vote2 = Vote(score=0, book=book, user=user1)
        vote2.save()

        # Comprobamos que el score no es la media, sino el nuevo score
        self.assertEqual(book.score, 0)
        self.assertEqual(book.num_votes, 1)