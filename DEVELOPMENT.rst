==============================================================================
Development Documentation
==============================================================================

Set up development environment
------------------------------

  $ virtualenv .env
  $ source .env/bin/activate
  $ python setup.py develop

Start 'MySite' Django application that is used to run the tests against::

  $ pip install Django
  $ python mysite/manage.py makemigrations
  $ python mysite/manage.py migrate
  $ python mysite/manage.py runserver

Run DjangoLibrary tests::

  $ python setup.py develop
  $ pybot DjangoLibrary/tests/autologin.robot


Generate Documentation
----------------------

  $ python -m robot.libdoc DjangoLibrary docs/DjangoLibrary.html

Release Documentation:

  $ git checkout gh-pages
  $ git commit . -m"Update keyword docs."
  $ git push
  $ git checkout master

Make Release
------------

  $ pip install zest.releaser
  $ fullrelease


Further Reading
---------------

http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.8.3#creating-test-libraries

https://docs.djangoproject.com/en/dev/howto/auth-remote-user/
