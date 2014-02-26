==============================================================================
A robot framework library for Django.
==============================================================================

.. image:: https://travis-ci.org/tisto/robotframework-djangolibrary.png?branch=master   :target: https://travis-ci.org/tisto/robotframework-djangolibrary


Introduction
------------

DjangoLibrary is a web testing library to test Django with Robot Framework.

It uses Selenium2Library to run tests against a real browser instance.


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

test.robot::

  *** Variables ***

  ${SERVER}               http://localhost:8000/
  ${BROWSER}              firefox


  *** Settings ***

  Documentation   Django Robot Tests
  Library         Selenium2Library  timeout=10  implicit_wait=0.5
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

  $ pybot test.robot


Output::

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
