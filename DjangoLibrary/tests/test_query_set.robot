*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              chrome


*** Settings ***

Documentation   Testing Query Keyword
Library         SeleniumLibrary  timeout=10  implicit_wait=0
Library         DjangoLibrary  127.0.0.1  55001  settings=mysite.robotframework_settings
Library         Collections
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

Test query without parameters
  Factory Boy  DjangoLibrary.tests.factories.UserFactory
  ${result}=  QuerySet  django.contrib.auth.models.User
  # Log List  ${result}  WARN
  ${user}=  Get From List  ${result}  0
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  johndoe
  Dictionary should contain item  ${user}  email  johndoe@example.com
  Dictionary should contain item  ${user}  is_superuser  False
  Dictionary should contain item  ${user}  is_staff  False

Test query with single parameter
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=janedoe
  ${result}=  QuerySet  django.contrib.auth.models.User  username=janedoe
  # Log List  ${result}  WARN
  ${user}=  Get From List  ${result}  0
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  janedoe

Test query with single parameter returns none
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=janedoe
  ${result}=  QuerySet  django.contrib.auth.models.User  username=johndoe
  # Log List  ${result}  WARN
  Length should be  ${result}  0

Test query with Book
  Factory Boy  bookstore.factories.BookFactory
  ${result}=  QuerySet  bookstore.models.Book
  # Log List  ${result}  WARN
  ${book}=  Get From List  ${result}  0
  Dictionary Should contain key  ${book}  title
  Dictionary should contain item  ${book}  title  Colorless Green Ideas Sleep Furiously

Test query with limit
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user1
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user2
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user3
  ${result}=  QuerySet  django.contrib.auth.models.User  limit=1
  # Log List  ${result}  WARN
  Length should be  ${result}  1
  ${user}=  Get From List  ${result}  0
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  user1

Test query with offset and limit
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user1
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user2
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user3
  ${result}=  QuerySet  django.contrib.auth.models.User  offset=1  limit=2
  # Log List  ${result}  WARN
  Length should be  ${result}  1
  ${user}=  Get From List  ${result}  0
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  user2

Test query with offset and limit (multiple results)
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user1
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user2
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user3
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user4
  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=user5
  ${result}=  QuerySet  django.contrib.auth.models.User  offset=2  limit=4
  # Log List  ${result}  WARN
  Length should be  ${result}  2
  ${user}=  Get From List  ${result}  0
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  user3
  ${user}=  Get From List  ${result}  1
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain item  ${user}  username  user4
