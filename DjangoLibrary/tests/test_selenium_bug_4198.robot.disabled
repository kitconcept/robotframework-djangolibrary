*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   Django Robot Tests
Library         Selenium2Library  timeout=10  implicit_wait=0
Library         DjangoLibrary  127.0.0.1  55001
Suite Setup     Start Django and Open Browser
Suite Teardown  Stop Django and Close Browser


*** Test Cases ***

Scenario: Type ü into input field
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Page Should Contain  Django administration
  Page Should Contain Element  name=username
  Page Should Contain Element  name=password
  Input Text  name=username  München
  Page should contain element  xpath=//input[@name='username' and @value='München']

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

Logout
  Go To  ${SERVER}/admin/logout
  Wait until page contains  Logged out
