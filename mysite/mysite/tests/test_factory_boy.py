from django.contrib.auth.models import User
from django.test import TestCase
from mysite.tests.factories import UserFactory
import datetime


class TestFactoryBoy(TestCase):

    def test_user_factory(self):
        user = UserFactory()
        self.assertTrue(isinstance(user, User))
        self.assertEqual('John', user.first_name)
        self.assertEqual('Doe', user.last_name)
        self.assertEqual('johndoe', user.username)
        self.assertEqual('johndoe@example.com', user.email)
        self.assertTrue(isinstance(user.date_joined, datetime.datetime))
