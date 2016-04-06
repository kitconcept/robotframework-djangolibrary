from django.contrib.auth.models import User
from django.test import TestCase
from DjangoLibrary.middleware import FactoryBoyMiddleware
from mock import Mock


class TestFactoryBoyMiddleware(TestCase):

    def setUp(self):
        self.cm = FactoryBoyMiddleware()
        self.request = Mock()
        self.request.session = {}

    def test_process_request_creates_object(self):
        setattr(self.request, 'FACTORY_BOY_MODEL_PATH', 'User')
        self.assertEqual(self.cm.process_request(self.request), None)
        self.assertEqual(1, len(User.objects.values()))
        self.assertEqual('johndoe', User.objects.values()[0]['username'])
