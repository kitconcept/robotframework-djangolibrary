*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   DjangoLibrary Autologin Tests
Library         Selenium2Library  timeout=10  implicit_wait=0
Library         DjangoLibrary  127.0.0.1  55001  path=mysite/mysite  manage=mysite/manage.py  settings=mysite.settings  db=mysite/db.sqlite3
Suite Setup     Start Django and Open Browser
Suite Teardown  Stop Django and Close Browser


*** Test Cases ***

Create superuser keyword should create superuser
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

Create superuser keyword should work with special characters
  Create Superuser  admin-öüä  admin@admin.com  password
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Input text  username  admin-öüä
  Input text  password  password
  Click Button  Log in
  Wait until page contains  Django administration
  Page should contain  Django administration
  Page should not contain  Please enter the correct username and password
  Logout

Create user keyword should create user
  Create User  test-user-1  test@test.com  password  is_superuser=True  is_staff=True
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Input text  username  test-user-1
  Input text  password  password
  Click Button  Log in
  Wait until page contains  Django administration
  Page should contain  Django administration
  Page should not contain  Please enter the correct username and password
  Logout

Create user keyword should work with special characters
  Create User  äüö-AÜÖ  test@test.com  password  is_superuser=True  is_staff=True
  Go To  ${SERVER}/admin
  Wait until page contains  Django administration
  Input text  username  äüö-AÜÖ
  Input text  password  password
  Click Button  Log in
  Wait until page contains  Django administration
  Page should contain  Django administration
  Page should not contain  Please enter the correct username and password
  Logout

Autologin keyword should login user
  Create User  test-user-2  test@test.com  password  is_superuser=True  is_staff=True
  Autologin as  test-user-2  password
  User is logged in

Autologin keyword should login user with special characters
  [tags]  current
  Create User  äüö-AÜÖ  test@test.com  password  is_superuser=True  is_staff=True
  Autologin as  äüö-AÜÖ  password
  User is logged in

Autologin keyword should work multiple times
  Autologin as  test-user-1  password
  Autologin as  test-user-2  password
  User 'test-user-2' is logged in

Autologin Logout keywords should log out user
  Create User  test-user-3  test@test.com  password  is_superuser=True  is_staff=True
  Autologin as  test-user-3  password
  User is logged in
  Autologin Logout
  User is logged out


*** Keywords ***

Start Django and open Browser
  Start Django
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django

Logout
  Go To  ${SERVER}/admin/logout
  Wait until page contains  Logged out

User is logged in
  Go To  ${SERVER}/admin
  Page should contain  Site administration  message=User is not logged in

User '${username}' is logged in
  Go To  ${SERVER}/admin
  Page should contain  ${username}  message=User '${username}' is not logged in

User is logged out
  Go To  ${SERVER}/admin
  Page should not contain  Site administration  message=User is not logged out
