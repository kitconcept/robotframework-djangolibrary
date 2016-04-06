# -*- coding: utf-8 -*-
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from warnings import warn

import base64
import json
import os
import requests
import signal
import subprocess

__version__ = '1.0'
ROBOT_LIBRARY_DOC_FORMAT = 'reST'


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
        """Create a regular Django user in the default auth model."""
        to_run = """
from django.contrib.auth.models import User
user = User.objects.create_user(
    %(username)s,
    email=%(email)s,
    password=%(password)s,
)
user.is_superuser = %(is_superuser)s
user.is_staff = %(is_staff)s
user.save()""" % {
            'username': repr(username.encode("utf-8")),
            'password': repr(password.encode("utf-8")),
            'email': repr(email),
            'is_superuser': repr(kwargs.get('is_superuser', False)),
            'is_staff': repr(kwargs.get('is_staff', False)),
        }

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
        django.communicate(to_run)

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

        """
        # robot keyword params are unicode. b64encode expects utf-8 strings
        username = username.encode("utf-8")
        password = password.encode("utf-8")
        # encode autologin cookie value as base64
        autologin_cookie_value = base64.b64encode(
            "%s:%s" % (username, password)
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
            "document.cookie = 'autologin=;path=/;domain=localhost;';")

    def factory_boy(self, factory, **kwargs):
        url = 'http://{}:{}'.format(
            self.host,
            self.port
        )
        payload = {
            'FACTORY_BOY_MODEL_PATH': factory,
            'FACTORY_BOY_ARGS': json.dumps(kwargs)
        }
        response = requests.get(url, params=payload)
        if response.status_code != 201:
            raise
        return response.json()
