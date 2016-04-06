*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   Testing Test Isolation
Library         Selenium2Library  timeout=10  implicit_wait=0.5
Library         DjangoLibrary  127.0.0.1  55001
Library         DebugLibrary
Suite Setup     Start Django and Open Browser
Suite Teardown  Stop Django and Close Browser
Test Teardown   Manage Flush


*** Keywords ***

Start Django and open Browser
  Start Django
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django


*** Test Cases ***

Test One: Create User
  Create User  test-user-1  test@test.com  password  is_superuser=True  is_staff=True
  Autologin as  test-user-1  password
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Page should contain  Site administration


Test Two: User from Test One should not be present
  Autologin as  test-user-1  password
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Page should not contain  Site administration
  Page should contain  Log in
