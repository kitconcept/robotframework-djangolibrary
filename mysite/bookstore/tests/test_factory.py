from django.test import TestCase
from ..models import Author
from ..models import Book
from ..factories import AuthorFactory
from ..factories import BookFactory


class TestFactoryBoy(TestCase):

    def test_author_factory(self):
        author = AuthorFactory()
        author.name = 'Noam Chomsky'
        self.assertTrue(isinstance(author, Author))

    def test_book_factory(self):
        book = BookFactory()
        book.name = 'Colorless Green Ideas Sleep Furiously'
        self.assertTrue(isinstance(book, Book))
