from django.contrib.auth.models import User
from django.test import TestCase
from DjangoLibrary.middleware import FactoryBoyMiddleware
from mock import Mock

import json


class TestFactoryBoyMiddleware(TestCase):

    def setUp(self):
        self.middleware = FactoryBoyMiddleware()
        self.request = Mock()
        self.request.session = {}

    def test_process_request_creates_object(self):
        self.request.configure_mock(
            **{
                'GET': {
                    'FACTORY_BOY_MODEL_PATH': 'mysite.tests.factories.UserFactory',  # noqa
                    'FACTORY_BOY_ARGS': ''
                }
            }
        )

        response = self.middleware.process_request(self.request)

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            'johndoe',
            json.loads(response.content).get('username')
        )
        self.assertEqual(1, len(User.objects.values()))
        self.assertEqual('johndoe', User.objects.values()[0]['username'])
