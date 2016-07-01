from factory import DjangoModelFactory
from .models import Author
from .models import Book
from .models import University
import factory


class UniversityFactory(DjangoModelFactory):
    class Meta:
        model = University
        django_get_or_create = ('name',)

    name = 'MIT'


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('name',)

    name = 'Noam Chomsky'
    university = factory.SubFactory(UniversityFactory)


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
        django_get_or_create = ('title',)

    title = 'Colorless Green Ideas Sleep Furiously'
    author = factory.SubFactory(AuthorFactory)
