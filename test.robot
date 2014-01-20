*** Variables ***

${SERVER}               http://localhost:8000/
${BROWSER}              firefox


*** Settings ***

Documentation   Django Robot Tests
Library         Selenium2Library  timeout=10  implicit_wait=0.5
Library         MyFirstDjangoLibrary
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
  My Keyword
  Start Django
  Stop Django
