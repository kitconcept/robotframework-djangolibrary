==============================================================================
A robot framework library for Django.
==============================================================================

.. image:: https://travis-ci.org/tisto/robotframework-djangolibrary.png?branch=master   :target: https://travis-ci.org/tisto/robotframework-djangolibrary


Installation
------------

  $ pip install robotframework-djangolibrary


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
