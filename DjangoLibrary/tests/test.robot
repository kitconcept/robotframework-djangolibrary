*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              chrome


*** Settings ***

Documentation   Django Robot Tests
Library         Selenium2Library  timeout=10  implicit_wait=0.5
Library         DjangoLibrary  127.0.0.1  55001  settings=mysite.robotframework_settings
Suite Setup     Start Django and Open Browser
Suite Teardown  Stop Django and Close Browser


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

Scenario: As a visitor I can visit the django admin login page
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Page Should Contain  Django administration
  Page Should Contain Element  name=username
  Page Should Contain Element  name=password
