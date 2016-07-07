# -*- coding: utf-8 -*-
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from warnings import warn

import base64
import json
import os
import requests
import signal
import six
import subprocess

__version__ = '1.0'
ROBOT_LIBRARY_DOC_FORMAT = 'reST'


def safe_bytes(str):
    """Returns bytes on Py3 and a string on Py2."""
    if six.PY3:
        return bytes(str, 'utf-8')
    else:
        return str


def safe_utf8(string):
    """Returns bytes on Py3 and an utf-8 encoded string on Py2."""
    if six.PY2:
        return string.encode("utf-8")
    else:
        return string


class DjangoLibrary:
    """DjangoLibrary is a web testing library to test Django with Robot
    Framework.

    It uses Selenium2Library to run tests against a real browser instance.

    *Before running tests*

    Prior to running test cases using DjangoLibrary, DjangoLibrary must be
    imported (together with Selenium2Library) into your Robot test suite
    (see `importing` section), and the Selenium2Library 'Open Browser' keyword
    must be used to open a browser to the desired location.
    """

    django_pid = None

    # TEST CASE => New instance is created for every test case.
    # TEST SUITE => New instance is created for every test suite.
    # GLOBAL => Only one instance is created during the whole test execution.
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, host="0.0.0.0", port=8000, path='mysite/mysite',
                 manage='mysite/manage.py', settings='mysite.settings',
                 db=None):
        """Django2Library can be imported with optional arguments.

        `host` is the hostname of your Django instance. Default value is
        '127.0.0.1'.

        `port` is the port number of your Django instance. Default value is
        8000.

        `path` is the path to your Django instance.

        `manage` is the path to your Django instance manage.py.

        `settings` is the path to your Django instance settings.py.

        `db` is deprecated. Please don't use it.

        Examples:
        | Library | Selenium2Library | timeout=15        | implicit_wait=0.5  | # Sets default timeout to 15 seconds and the default implicit_wait to 0.5 seconds. |  # noqa
        | Library | DjangoLibrary    | 127.0.0.1         | 55001              | path=mysite/mysite | manage=mysite/manage.py | settings=mysite.settings | db=mysite/db.sqlite3 | # Sets default hostname to 127.0.0.1 and the default port to 55001.                |  # noqa
        """
        self.host = host
        self.port = port
        self.path = os.path.realpath(path)
        self.manage = os.path.realpath(manage)
        self.settings = settings
        if db:
            warn(
                "Using the DjangoLibrary 'db' parameter is deprecated. " +
                "Use the 'settings' parameter instead to set a " +
                "database connection."
            )

    def manage_makemigrations(self):
        """Create migrations by running 'python manage.py makemigrations'."""
        args = [
            'python',
            self.manage,
            'makemigrations',
        ]
        subprocess.call(args)

    def manage_migrate(self):
        """Execute migration by running 'python manage.py migrate'."""
        args = [
            'python',
            self.manage,
            'migrate',
        ]
        subprocess.call(args)

    def manage_flush(self):
        """Clear database by running 'python manage.py flush'."""
        args = [
            'python',
            self.manage,
            'flush',
            '--noinput',
        ]
        subprocess.call(args)

    def clear_db(self):
        """Clear database. This is a legacy keyword now. Use 'Manage Flush'
           instead.
        """
        warn(
            "The DjangoLibrary 'clear_db' keyword is deprecated. " +
            "Use the 'manage_flush' keyword instead."
        )
        self.manage_flush()

    def create_user(self, username, email, password, **kwargs):
        """Create a regular Django user in the default auth model.

        The `Create User` keyword allows to provide additional arguments that
        are passed directly to the Djange create_user method (e.g.
        "is_staff=True")."""

        to_run = """
from django.contrib.auth.models import User
user = User.objects.create_user(
    '{0}',
    email='{1}',
    password='{2}',
)
user.is_superuser = '{3}'
user.is_staff = '{4}'
user.save()""".format(
            safe_utf8(username),
            safe_utf8(email),
            safe_utf8(password),
            kwargs.get('is_superuser', False),
            kwargs.get('is_staff', False),
        )
        args = [
            'python',
            self.manage,
            'shell',
            '--plain',
            '--settings=%s' % self.settings,
        ]

        django = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        django.communicate(safe_bytes(to_run))

    def create_superuser(self, username, email, password):
        """Create a Django superuser in the default auth model."""
        self.create_user(username, email, password,
                         is_superuser=True, is_staff=True)

    def start_django(self):
        """Start the Django server."""
        self.clear_db()
        self.manage_makemigrations()
        self.manage_migrate()
        logger.console("-" * 78)
        args = [
            'python',
            self.manage,
            'runserver',
            '%s:%s' % (self.host, self.port),
            '--nothreading',
            '--noreload',
            '--settings=%s' % self.settings,
        ]

        self.django_pid = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).pid
        logger.console(
            "Django started (PID: %s)" % self.django_pid,
        )
        logger.console("-" * 78)

    def stop_django(self):
        """Stop the Django server."""
        os.kill(self.django_pid, signal.SIGKILL)
        logger.console(
            "Django stopped (PID: %s)" % self.django_pid,
        )
        logger.console("-" * 78)

    def autologin_as(self, username, password):
        """Autologin as Django user.

        DjangoLibrary comes with a Django middleware component that allows the
        autologin_as keyword to set an 'autologin' cookie that the
        middleware uses to authenticate and login the user in Django.

        If you want to use the autlogin_as keyword you have to add
        'DjangoLibrary.middleware.AutologinAuthenticationMiddleware' to the
        MIDDLEWARE_CLASSES right after the default AuthenticationMiddleware
        in your settings.py::

            MIDDLEWARE_CLASSES = (
                ...
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'DjangoLibrary.middleware.AutologinAuthenticationMiddleware',
            )

        *Warning*

        Make sure that you add this middleware only to your test setup and
        NEVER to your deployment!

        See https://github.com/kitconcept/robotframework-djangolibrary/blob/master/DjangoLibrary/tests/test_autologin.robot  # noqa
        for examples how to use the `Autologin As` keyword.

        """
        if six.PY2:
            username = username.encode('utf-8')
            password = password.encode('utf-8')
        # encode autologin cookie value as base64
        autologin_cookie_value = base64.b64encode(
            safe_bytes("%s:%s" % (username, password))
        )

        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        # XXX: The 'Add Cookie' keywords does not work with Firefox, therefore
        # we have to add the cookie with js here. A bug has been filed:
        # https://github.com/rtomac/robotframework-selenium2library/issues/273
        # selenium2lib.add_cookie(
        #     "autologin",
        #     "%s:%s" % (username, password),
        #     path="/",
        #     domain="localhost",
        # )

        if six.PY3:
            selenium2lib.execute_javascript(
                "document.cookie = 'autologin=%s;path=/;domain=localhost;';" %
                autologin_cookie_value.decode('utf-8')
            )
        else:
            selenium2lib.execute_javascript(
                "document.cookie = 'autologin=%s;path=/;domain=localhost;';" %
                autologin_cookie_value
            )

        # autologin_cookie = selenium2lib.get_cookie_value('autologin')
        # assert autologin_cookie == "%s:%s" % (username, password)
        # cookies = selenium2lib.get_cookies()
        # assert cookies == u"autologin=%s:%s" % (username, password)

    def autologin_logout(self):
        """Logout a user that has been logged in by the autologin_as keyword.
        """
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        selenium2lib.execute_javascript(
            "document.cookie = 'autologin=;path=/;domain=localhost;';"
        )

    def factory_boy(self, factory, **kwargs):
        """Create content objects in the Django database with Factory Boy.
        See https://factoryboy.readthedocs.org for more details.

        Arguments:

        `factory` is a required argument and should contain the full path to
        your factory boy factory class (e.g.
        "FactoryBoy mysite.polls.factories.PollFactory").

        The `Factory Boy` keyword allows to provide additional arguments that
        are passed directly to the Factory Boy Factory class
        (e.g. "FactoryBoy mysite.polls.factories.PollFactory pollname='mypoll'").

        You can also override subfactories by using the double-underscore
        field lookup (https://docs.djangoproject.com/en/1.9/topics/db/queries/#field-lookups)  #noqa
        together with the `pk` lookup shortcut (https://docs.djangoproject.com/en/1.9/topics/db/queries/#the-pk-lookup-shortcut)
        (e.g. "Factory Boy  bookstore.factories.BookFactory ... author__pk=1")

        See https://github.com/kitconcept/robotframework-djangolibrary/blob/master/DjangoLibrary/tests/test_factory_boy.robot  # noqa
        for examples how to use the `Factory Boy` keyword.

        """
        url = 'http://{}:{}'.format(
            self.host,
            self.port
        )
        payload = {
            'FACTORY_BOY_MODEL_PATH': factory,
            'FACTORY_BOY_ARGS': json.dumps(kwargs)
        }
        response = requests.get(url, params=payload)
        if response.status_code == 201:
            return response.json()
        status_code_400 = response.status_code == 400
        type_json = response.headers.get('Content-Type') == 'application/json'
        if status_code_400 and type_json:
            msg = response.json().get('error', '')
            traceback = response.json().get('traceback', '')
            if traceback:
                msg = msg + '\n\n' + traceback
            raise requests.exceptions.HTTPError(msg, response=response)
        return response.raise_for_status()

    def query_set(self, model, **kwargs):
        """Query the Django ORM.

        Returns a QuerySet object. See https://docs.djangoproject.com/en/1.9/topics/db/queries/#retrieving-objects for details.  # noqa

        Arguments:

        `model` is a required argument and should contain the full path to
        your Django model class (e.g. "django.contrib.auth.models.User").

        The `QuerySet` keyword allows to provide additional arguments that
        are passed as filter arguments
        (e.g. "django.contrib.auth.models.User  username=john").
        If no additonal argument is provided `QuerySet will just return all
        objects that exists for that model.

        `limit` limits the number of results,
        e.g. "django.contrib.auth.models.User  limit=10" will return 10 results
        max.
        Limit is an optional argument that maps 1:1 to the QuerySet limit
        argument. See https://docs.djangoproject.com/en/1.9/topics/db/queries/#limiting-querysets  # noqa
        for details.

        `offset` can be used in combination with `limit` to set an offset,
        e.g. "django.contrib.auth.models.User  offeset=5  limit=10" will return
        5 results while omitting the first 5 results.
        See https://docs.djangoproject.com/en/1.9/topics/db/queries/#limiting-querysets  # noqa
        for details.

        See https://github.com/kitconcept/robotframework-djangolibrary/blob/master/DjangoLibrary/tests/test_query_set.robot  # noqa
        for examples how to use the `Query Set` keyword.

        """
        url = 'http://{}:{}'.format(
            self.host,
            self.port
        )
        payload = {
            'MODEL_PATH': model,
            'QUERY_ARGS': json.dumps(kwargs)
        }
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            return response.json()
        status_code_400 = response.status_code == 400
        type_json = response.headers.get('Content-Type') == 'application/json'
        if status_code_400 and type_json:
            msg = response.json().get('error', '')
            traceback = response.json().get('traceback', '')
            if traceback:
                msg = msg + '\n\n' + traceback
            raise requests.exceptions.HTTPError(msg, response=response)
        return response.raise_for_status()
