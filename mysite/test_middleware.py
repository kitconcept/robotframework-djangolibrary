from django.contrib.auth.models import User
from django.test import TestCase
from DjangoLibrary.middleware import CreateContentMiddleware
from mock import Mock


class TestCreateContentMiddleware(TestCase):

    def setUp(self):
        self.cm = CreateContentMiddleware()
        self.request = Mock()
        self.request.session = {}

    def test_process_request_creates_object(self):
        setattr(self.request, 'ROBOTFRAMEWORK_DJANGO_MODEL_NAME', 'User')
        self.assertEqual(self.cm.process_request(self.request), None)
        self.assertEqual(1, len(User.objects.values()))
        self.assertEqual('johndoe', User.objects.values()[0]['username'])
