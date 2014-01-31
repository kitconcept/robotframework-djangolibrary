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

Logout
  Go To  ${SERVER}/admin/logout
  Wait until page contains  Logged out


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
  Logout

Scenario: Create user
  Create User  test-user-1  test@test.com  password  is_superuser=True  is_staff=True
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Input text  username  test-user-1
  Input text  password  password
  Click Button  Log in
  Wait until page contains  Django administration
  Page should contain  Django administration
  Page should not contain  Please enter the correct username and password
