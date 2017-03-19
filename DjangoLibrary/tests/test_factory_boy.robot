*** Variables ***

${SERVER}               http://localhost:55001
${BROWSER}              firefox


*** Settings ***

Documentation   Testing Test Isolation
Library         Selenium2Library  timeout=10  implicit_wait=0
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

Factory Boy Keyword Should Return Object
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory
  Dictionary Should Contain Key  ${user}  username
  Dictionary should contain key  ${user}  password
  Dictionary should contain item  ${user}  username  johndoe
  Dictionary should contain item  ${user}  email  johndoe@example.com
  Dictionary should contain item  ${user}  is_superuser  False
  Dictionary should contain item  ${user}  is_staff  False

Factory Boy Keyword Should Return Primary Key Attribute
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory

  Dictionary should contain key  ${user}  pk

Factory Boy Keyword Should Override Attributes
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory
  ...  username=janedoe

  Dictionary should contain item  ${user}  username  janedoe
  Dictionary should contain item  ${user}  email  janedoe@example.com

Factory Boy Keyword Should Override Multiple Attributes
  ${user}=  Factory Boy  DjangoLibrary.tests.factories.UserFactory
  ...  username=janedoe
  ...  email=jane@doe.com

  Dictionary should contain item  ${user}  username  janedoe
  Dictionary should contain item  ${user}  email  jane@doe.com

Factory Boy Keyword Should Work For Author
  ${author}=  Factory Boy  bookstore.factories.AuthorFactory
  Dictionary Should Contain Key  ${author}  name
  Dictionary should contain item  ${author}  name  Noam Chomsky

Factory Boy Keyword Should Work For Book
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  Colorless Green Ideas Sleep Furiously

Factory Boy Keyword Should Get Or Create An Object
  # Create two authors with the same name
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  # The author should not be created twice
  ${result}=  QuerySet  bookstore.models.Author  name=Howard Zinn
  Length should be  ${result}  1

Factory Boy Keyword Should Work With Subfactory
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__name=Howard Zinn
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Factory Boy Keyword Should Work With Subfactory Subfactory
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__name=Howard Zinn
  ...  author__university__name=Boston University
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author
  ${result}=  QuerySet  bookstore.models.University  name=Boston University
  Length should be  ${result}  1

Factory Boy Keyword Should Work With Subfactory and Existing Content
  ${author}=  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${author_id}=  Get From Dictionary  ${author}  id
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__pk=${author_id}
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Factory Boy Keyword Should Work With Subfactory, Existing Content, and QuerySet Lookup
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${authors}=  QuerySet  bookstore.models.Author  name=Howard Zinn
  ${author}=  Get From List  ${authors}  0
  ${author_id}=  Get From Dictionary  ${author}  id
  ${book}=  Factory Boy  bookstore.factories.BookFactory
  ...  title=A People's History of the United States
  ...  author__pk=${author_id}
  Dictionary Should Contain Key  ${book}  title
  Dictionary should contain item  ${book}  title  A People's History of the United States
  Dictionary Should Contain Key  ${book}  author

Factory Boy Keyword Should Work With Subfactory And Reuse Of Existing Content
  # Ensure that exactly one Howard Zinn exists
  Factory Boy  bookstore.factories.AuthorFactory  name=Howard Zinn
  ${authors}=  QuerySet  bookstore.models.Author  name=Howard Zinn
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
  ${authors}=  QuerySet  bookstore.models.Author  name=Howard Zinn
  Length Should Be    ${authors}    1

Factory Boy Keyword Should Raise an Exception If Path Does Not Exist
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: Factory Boy class "Non.Existing.Path" could not be found
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  Non.Existing.Path

Factory Boy Keyword Should Raise an Exception On Broken Class
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactory"
  ...  could not be instantiated with args "{}"
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactory

Factory Boy Keyword Should Raise an Exception On Class Without Meta Class
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactoryWithoutMetaClass"
  ...  could not be instantiated with args "{}"
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactoryWithoutMetaClass

Factory Boy Keyword Should Raise an Exception If Class Does Not Inherit From DjangoModelFactory
  ${expected_error}=  catenate  SEPARATOR=${SPACE}
  ...  HTTPError: The FactoryBoyClass
  ...  "DjangoLibrary.tests.factories.BrokenFactoryClassDoesNotInheritFromDjangoModelFactory"
  ...  instance does not seem to provide a _meta attribute.
  ...  Please check if the Factory Boy class inherits from DjangoModelFactory
  Run Keyword and Expect Error  ${expected_error}  Factory Boy  DjangoLibrary.tests.factories.BrokenFactoryClassDoesNotInheritFromDjangoModelFactory
