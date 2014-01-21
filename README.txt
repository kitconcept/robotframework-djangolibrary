==============================================================================
How To Test a Django App with Robot Framework
==============================================================================

Basic Setup
-----------

  $ mkdir robot-testing
  $ cd robot-testing
  $ virtualenv .env
  $ source .env/bin/activate


Robot Framework Installation
----------------------------

requirements.txt::

  robotframework
  robotframework-selenium2library

pip install -r requirements.txt


Django Installation
-------------------

  $ pip install django
  $ django-admin.py startproject mysite


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


Start Django
------------

  $ cd mysite
  $ python manage.py runserver


Run Robot Tests
---------------

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
  Output:  /home/timo/workspace/prounix/robot-testing/output.xml
  Log:     /home/timo/workspace/prounix/robot-testing/log.html
  Report:  /home/timo/workspace/prounix/robot-testing/report.html


Further Reading
---------------

http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html?r=2.8.3#creating-test-libraries
