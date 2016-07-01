from django.contrib.auth.models import User
from django.test import TestCase
from DjangoLibrary.middleware import QueryMiddleware
from mock import Mock

import json


class TestQueryMiddleware(TestCase):

    def setUp(self):
        self.middleware = QueryMiddleware()
        self.request = Mock()
        self.request.session = {}

    def test_query(self):
        self.request.configure_mock(
            **{
                'GET': {
                    'MODEL_PATH': 'django.contrib.auth.models.User',
                    'ARGS': ''
                }
            }
        )

        john = User(username='john', email='john@doe.com')
        john.save()
        response = self.middleware.process_request(self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            'john',
            json.loads(response.content.decode('utf-8'))[0].get('username')
        )
        self.assertEqual(
            'john@doe.com',
            json.loads(response.content.decode('utf-8'))[0].get('email')
        )

    def test_empty_query(self):
        self.request.configure_mock(
            **{
                'GET': {
                    'MODEL_PATH': 'django.contrib.auth.models.User',
                    'QUERY_ARGS': '{"username": "jane"}'
                }
            }
        )

        john = User(username='john', email='john@doe.com')
        john.save()
        response = self.middleware.process_request(self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            0,
            len(json.loads(response.content.decode('utf-8'))),
            'Query result should be empty when querying for username "jane"'
        )
