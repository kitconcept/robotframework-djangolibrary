*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   Testing Test Isolation
Library         Selenium2Library  timeout=10  implicit_wait=0
Library         DjangoLibrary  127.0.0.1  55001
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

Test Factory Boy Keyword
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory
  # Log Dictionary  ${user}  WARN
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain key  ${user}  password
  Dictionary should contain item  ${user}  username  johndoe
  Dictionary should contain item  ${user}  email  johndoe@example.com
  Dictionary should contain item  ${user}  is_superuser  False
  Dictionary should contain item  ${user}  is_staff  False

Test Factory Boy Keyword Override Single Attribute
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=janedoe
  # Log Dictionary  ${user}  WARN
  Dictionary should contain item  ${user}  username  janedoe
  Dictionary should contain item  ${user}  email  janedoe@example.com

Test Factory Boy Keyword Override Multiple Attribute
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory  username=janedoe  email=jane@doe.com
  # Log Dictionary  ${user}  WARN
  Dictionary should contain item  ${user}  username  janedoe
  Dictionary should contain item  ${user}  email  jane@doe.com

Test Factory Boy Keyword for Author
  ${author}=  Factory Boy  bookstore.factories.AuthorFactory
  # Log Dictionary  ${user}  WARN
  Dictionary Should Contain Key  ${author}  name
  Dictionary should contain item  ${author}  name  Noam Chomsky

Test Factory Boy Keyword for Book
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  # Log Dictionary  ${user}  WARN
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  Colorless Green Ideas Sleep Furiously

Test Factory Boy Get Or Create
  # Create two authors with the same name
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  # The author should not be created twice
  ${result}=  Query  bookstore.models.Author  name=Howard Zinn
  Length should be  ${result}  1

Test Factory Boy Class with Subfactory
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__name=Howard Zinn
  # Log Dictionary  ${book}  Warn
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Test Factory Boy Class with Subfactory Subfactory
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__name=Howard Zinn
  ...  author__university__name=Boston University
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author
  ${result}=  Query  bookstore.models.University  name=Boston University
  Length should be  ${result}  1

Test Factory Boy Class with Subfactory and Existing Content
  ${author}=  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${author_id}=  Get From Dictionary  ${author}  id
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__pk=${author_id}
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Test Factory Boy Class with Subfactory and Existing Content with Query Lookup
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${authors}=  Query  bookstore.models.Author  name=Howard Zinn
  ${author}=  Get From List  ${authors}  0
  ${author_id}=  Get From Dictionary  ${author}  id
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__pk=${author_id}
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Test Factory Boy Class with Subfactory and reuse of existing data
  # Ensure that exactly one Howard Zinn exists
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${authors}=  Query  bookstore.models.Author  name=Howard Zinn
  Length Should Be  ${authors}  1

  # Create a Book with author__name=Howard Zinn
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__name=Howard Zinn
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

  # Ensure that call to the BookFactory did not create another
  # entry on the Author table, but reused the existing author
  ${authors}=  Query  bookstore.models.Author  name=Howard Zinn
  Length Should Be    ${authors}    1

Test Factory Boy with non-existing path raises Exception
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: Factory Boy class "Non.Existing.Path" could not be found
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  Non.Existing.Path

Test Factory Boy with broken class raises Exception
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactory"
  ...  could not be instantiated with args "{}"
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactory

Test Factory Boy class without meta class
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactoryWithoutMetaClass"
  ...  could not be instantiated with args "{}"
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactoryWithoutMetaClass

Test Factory Boy class does not inherit from DjangoModelFactory
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: The FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactoryClassDoesNotInheritFromDjangoModelFactory"
  ...  instance does not seem to provide a _meta attribute.
  ...  Please check if the Factory Boy class inherits from DjangoModelFactory
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactoryClassDoesNotInheritFromDjangoModelFactory
