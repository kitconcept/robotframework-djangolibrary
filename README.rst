==============================================================================
A robot framework library for Django.
==============================================================================

.. image:: https://travis-ci.org/kitconcept/robotframework-djangolibrary.png?branch=master :target: https://travis-ci.org/kitconcept/robotframework-djangolibrary


Introduction
------------

DjangoLibrary is a web testing library to test Django with Robot Framework. It uses Selenium2Library to run tests against a real browser instance.


Installation
------------

  $ pip install robotframework-djangolibrary

In order to be able to use DjangoLibrary's autologin keywords you have to add
the AutologinAuthenticationMiddleware to your MIDDLEWARE_CLASSES in your
settings.py::

  MIDDLEWARE_CLASSES = (
      ...
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'DjangoLibrary.middleware.AutologinAuthenticationMiddleware',
  )

.. DANGER::
   Make sure that you add this middleware only to your test setup and
   NEVER to your deployment! The middleware just checks for a 'autologin'
   cookie and then authenticates and login ANY user.


First Robot Test
----------------

In order to write your first robot test, make sure that you include Selenium2Library and DjangoLibrary. Create a test.robot file with the
following content::

  *** Variables ***

  ${SERVER}               http://localhost:8000/
  ${BROWSER}              firefox


  *** Settings ***

  Documentation   Django Robot Tests
  Library         Selenium2Library  timeout=10  implicit_wait=0.5
  Library         DjangoLibrary  127.0.0.1  8080
  Suite Setup     Open Browser To Login Page
  Suite Teardown  Close Browser


  *** Keywords ***

  Open Browser To Login Page
    Open Browser  ${SERVER}  ${BROWSER}
    Maximize Browser Window


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


Development
-----------

Checkout repository from github::

  $ git clone https://github.com/kitconcept/robotframework-djangolibrary.git

Create a virtual Python environment::

  $ cd robotframework-djangolibrary/
  $ virtualenv .env
  $ source .env/bin/activate

Install robotframework-djangolibrary in development mode::

  $ python setup.py develop

Install the requirements::

  $ pip install -r requirements.txt

Run robotframework-djangolibrary tests::

  $ pybot DjangoLibrary/tests/
