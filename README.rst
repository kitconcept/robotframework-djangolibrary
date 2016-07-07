==============================================================================
A robot framework library for Django.
==============================================================================

.. image:: https://travis-ci.org/kitconcept/robotframework-djangolibrary.svg?branch=master
    :target: https://travis-ci.org/kitconcept/robotframework-djangolibrary

.. image:: https://img.shields.io/pypi/dm/robotframework-djangolibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-djangolibrary/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/robotframework-djangolibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-djangolibrary/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/robotframework-djangolibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-djangolibrary/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/l/robotframework-djangolibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-djangolibrary/
    :alt: License


Introduction
------------

DjangoLibrary is a web testing library to test Django with Robot Framework. It uses Selenium2Library to run tests against a real browser instance.

The library will automatically start and stop your Django instance while running the tests. It also comes with serveral autologin keywords that allow you to login different users during your tests, without the need to actually access the login page.

DjangoLibrary is tested against Django 1.8.x and 1.9.x with SQLite and Postgres on Python 2.7 and 3.5.


Documentation
-------------

`Robot Framework Django Library Keyword Documentation`_


Installation
------------

Install robotframework-djangolibrary with pip::

  $ pip install robotframework-djangolibrary

In order to be able to use DjangoLibrary's `Autologin`, `FactoryBoy`, or
`QuerySet` keywords you have to add the corresponding middleware classes to
your MIDDLEWARE_CLASSES in yoursettings.py::

  MIDDLEWARE_CLASSES = (
      ...
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'DjangoLibrary.middleware.AutologinAuthenticationMiddleware',
      'DjangoLibrary.middleware.FactoryBoyMiddleware',
      'DjangoLibrary.middleware.QuerySetMiddleware',
  )

.. DANGER::
   Make sure that you add those middlewares only to your test setup and
   NEVER to your deployment! The Autologin middleware just checks for a
   'autologin' cookie and then authenticates and login ANY user.


First Robot Test
----------------

In order to write your first robot test, make sure that you include Selenium2Library and DjangoLibrary. Create a test.robot file with the
following content::

  *** Variables ***

  ${HOSTNAME}             127.0.0.1
  ${PORT}                 55001
  ${SERVER}               http://${HOSTNAME}:${PORT}/
  ${BROWSER}              firefox


  *** Settings ***

  Documentation   Django Robot Tests
  Library         Selenium2Library  timeout=10  implicit_wait=0
  Library         DjangoLibrary  ${HOSTNAME}  ${PORT}  path=mysite/mysite  manage=mysite/manage.py  settings=mysite.settings  db=mysite/db.sqlite3
  Suite Setup     Start Django and open Browser
  Suite Teardown  Stop Django and close Browser


  *** Keywords ***

  Start Django and open Browser
    Start Django
    Open Browser  ${SERVER}  ${BROWSER}

  Stop Django and close browser
    Close Browser
    Stop Django


  *** Test Cases ***

  Scenario: As a visitor I can visit the django default page
    Go To  ${SERVER}
    Wait until page contains element  id=explanation
    Page Should Contain  It worked!
    Page Should Contain  Congratulations on your first Django-powered page.


Run Tests
---------

Then you can run the test with pybot::

  $ pybot test.robot

The output should look like this::

  ==============================================================================
  Test :: Django Robot Tests
  ==============================================================================
  Scenario: As a visitor I can visit the django default page            | PASS |
  ------------------------------------------------------------------------------
  Test :: Django Robot Tests                                            | PASS |
  1 critical test, 1 passed, 0 failed
  1 test total, 1 passed, 0 failed
  ==============================================================================
  Output:  /home/timo/workspace/prounix/robotframework-djangolibrary/output.xml
  Log:     /home/timo/workspace/prounix/robotframework-djangolibrary/log.html
  Report:  /home/timo/workspace/prounix/robotframework-djangolibrary/report.html


Test Isolation
--------------

robotframework-djangolibrary does not provide isolation between tests by
default. This means if you add an object to the database in a test, this
object will be present in the next test as well. You need to cleanup
yourself in order to have a proper isolation between the tests. You can use
the robotframework "Test Teardown" call to call the "Clear DB" keyword after
each test::

  *** Settings ***

  Library         Selenium2Library  timeout=10  implicit_wait=0
  Library         DjangoLibrary  ${HOSTNAME}  ${PORT}  path=mysite/mysite  manage=mysite/manage.py  settings=mysite.settings  db=mysite/db.sqlite3
  Suite Setup     Start Django and open Browser
  Suite Teardown  Stop Django and close Browser
  Test Teardown   Clear DB


Development
-----------

Checkout repository from github::

  $ git clone https://github.com/kitconcept/robotframework-djangolibrary.git

Create a virtual Python environment::

  $ cd robotframework-djangolibrary/
  $ virtualenv .py27
  $ source .py27/bin/activate

Install robotframework-djangolibrary in development mode::

  $ python setup.py develop

Install the requirements::

  $ pip install -r requirements.txt

Run Unit/Integration-Tests::

  $ pytest mysite/

Run Acceptance Tests::

  $ pybot DjangoLibrary/tests/

.. _`Robot Framework Django Library Keyword Documentation`: https://kitconcept.github.io/robotframework-djangolibrary/DjangoLibraryDocs.html
