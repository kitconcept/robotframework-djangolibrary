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
Test Teardown   Clear DB


*** Keywords ***

Start Django and open Browser
  Start Django
  Open Browser  ${SERVER}  ${BROWSER}

Stop Django and close browser
  Close Browser
  Stop Django


*** Test Cases ***

Simple
  ${user}=  Create content  factory=User
  ${user}.username != ''
  ${user}.password != ''

Relationship Simple Style
  ${role}=  Create content  factory=Role  name=Guest
  ${user}=  Create content  factory=User  username=johndoe  role=${role}

Relationship Django Style
  ${role}=  Create content  factory=Role  name=Guest
  ${user}=  Create content  factory=User  username=johndoe  role__name=Guest

Relationship Auto generate submodels
  ${user}=  Create content  factory=User  username=johndoe
  QUERY SQL  user.role != None

Relationship Auto generate submodels with parameters create
  QUERY SQL  role.guest count 0
  ${user}=  Create content  factory=User  username=johndoe  role__name=Guest
  QUERY SQL  role count = 1
  QUERY SQL  role.name = Guest

Relationship Auto generate submodels with parameters get or create
  ${role}=  Create content  factory=Role  name=Guest
  ${user}=  Create content  factory=User  username=johndoe  role__name=Guest
  QUERY SQL  role count = 1
  QUERY SQL  role.name = Guest
