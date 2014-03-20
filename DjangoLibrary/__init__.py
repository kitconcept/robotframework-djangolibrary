# -*- coding: utf-8 -*-
__version__ = '0.1'

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

import os
import sys
import signal
import subprocess

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

    def __init__(self, host="127.0.0.1", port=8000):
        """Django2Library can be imported with optional arguments.

        `host` is the hostname of your Django instance. Default value is
        '127.0.0.1'.

        `port` is the port number of your Django instance. Default value is
        8000.

        Examples:
        | Library | Selenium2Library | timeout=15        | implicit_wait=0.5  | # Sets default timeout to 15 seconds and the default implicit_wait to 0.5 seconds. |  # noqa
        | Library | DjangoLibrary    | 127.0.0.1         | 55001              | # Sets default hostname to 127.0.0.1 and the default port to 55001.                |  # noqa
        """
        self.host = host
        self.port = port

    def clear_db(self):
        """Clear the Django default database by running
        'python manage.py syncdb'.
        """
        # XXX: Flush seems to be not working
        #args = [
        #    'python',
        #    'mysite/manage.py',
        #    'flush',
        #    '--noinput',
        #]
        args = [
            'rm',
            'mysite/db.sqlite3',
        ]
        subprocess.call(args)
        args = [
            'python',
            'mysite/manage.py',
            'syncdb',
            '--noinput',
        ]
        subprocess.call(args)

    def create_user(self, username, email, password, **kwargs):
        """Create a regular Django user in the default auth model."""
        sys.path.append(os.path.dirname(os.path.realpath('mysite/mysite')))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username,
            email=email,
            password=password,
        )
        user.is_superuser = kwargs.get('is_superuser', False)
        user.is_staff = kwargs.get('is_staff', False)
        user.save()

    def create_superuser(self, username, email, password):
        """Create a Django superuser in the default auth model."""
        sys.path.append(os.path.dirname(os.path.realpath('mysite/mysite')))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        from django.contrib.auth.models import User
        user = User.objects.create_superuser(
            username,
            email=email,
            password=password,
        )
        user.save()

    def start_django(self):
        """Start the Django server."""
        self.clear_db()
        logger.console("-" * 78)
        args = [
            'python',
            'mysite/manage.py',
            'runserver',
            '%s:%s' % (self.host, self.port),
            '--nothreading',
            '--noreload',
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
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        selenium2lib.add_cookie(
            "autologin",
            "%s:%s" % (username, password),
            path="/",
            domain="localhost",
        )
        # XXX: The 'Add Cookie' keywords does not work with Firefox, therefore
        # we have to add the cookie with js here. A bug has been filed:
        # https://github.com/rtomac/robotframework-selenium2library/issues/273
        selenium2lib.execute_javascript(
            "document.cookie = 'autologin=%s:%s;path=/;domain=localhost;';" %
            (username, password)
        )
        autologin_cookie = selenium2lib.get_cookie_value('autologin')
        assert autologin_cookie == "%s:%s" % (username, password)
        cookies = selenium2lib.get_cookies()
        assert cookies == u"autologin=%s:%s" % (username, password)

    def autologin_logout(self):
        """Logout a user that has been logged in by the autologin_as keyword.
        """
        selenium2lib = BuiltIn().get_library_instance('Selenium2Library')
        selenium2lib.execute_javascript(
            "document.cookie = 'autologin=;path=/;domain=localhost;';")

    def pause(self):
        """Visually pause test execution with interactive dialog by importing
        **Dialogs**-library and calling its **Pause Execution**-keyword.
        """
        from robotframework.libraries.Dialogs import pause_execution
        pause_execution()

    def debug(self):
        """Pause test execution with interactive debugger (REPL) in the
        current shell.

        This keyword is based on ``roboframework-debuglibrary``
        and requires that the used Python is compiled with
        ``readline``-support.
        """
        from robotframework_debuglibrary.DebugLibrary import Debug
        Debug()
