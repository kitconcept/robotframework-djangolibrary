# -*- coding: utf-8 -*-
__version__ = '0.1'

from robot.api import logger

import os
import sys
import signal
import subprocess

ROBOT_LIBRARY_DOC_FORMAT = 'reST'


class DjangoLibrary:
    """A library for testing Django with Robot Framework.
    """

    django_pid = None
    selenium_pid = None

    # TEST CASE => New instance is created for every test case.
    # TEST SUITE => New instance is created for every test suite.
    # GLOBAL => Only one instance is created during the whole test execution.
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port

    def clear_db(self):
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

    def create_superuser(self, username, email, password):
        sys.path.append(os.path.dirname(os.path.realpath('mysite/mysite')))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        from django.contrib.auth.models import User
        user = User.objects.create_superuser(
            'admin',
            email='admin@admin.com',
            password='admin'
        )
        user.save()
        logger.console("Create User: %s" % username)

    def start_django(self):
        """Start the Django server."""
        self.clear_db()
        args = [
            'python',
            'mysite/manage.py',
            'runserver',
            '%s:%s' % (self.host, self.port),
            '--nothreading',
            '--noreload',
        ]
        self.django_pid = subprocess.Popen(args).pid
        logger.console(
            "Django started (PID: %s)" % self.django_pid,
        )
        self.create_superuser("admin", "admin@admin.com", "admin")

    def stop_django(self):
        """Stop Django server."""
        os.kill(self.django_pid, signal.SIGKILL)
        logger.console(
            "Django stopped (PID: %s)" % self.django_pid,
        )
