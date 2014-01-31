*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   Django Robot Tests
Library         Selenium2Library  timeout=10  implicit_wait=0.5
Library         DjangoLibrary  127.0.0.1  55001
Suite Setup     Start Django and Open Browser
Suite Teardown  Stop Django and Close Browser


*** Keywords ***

Start Django and open Browser
  Start Django
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django

Pause
  Import library  Dialogs
  Pause execution


*** Test Cases ***

Scenario: Create superuser
  Create Superuser  admin  admin@admin.com  password
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Input text  username  admin
  Input text  password  password
  Click Button  Log in
  Wait until page contains  Django administration
  Page should contain  Django administration
  Page should not contain  Please enter the correct username and password
