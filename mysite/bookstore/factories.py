from factory import DjangoModelFactory
from .models import Author
from .models import Book

import factory


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('name',)

    name = 'Noam Chomsky'


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
        django_get_or_create = ('title',)

    title = 'Colorless Green Ideas Sleep Furiously'
    author = factory.SubFactory(AuthorFactory)
