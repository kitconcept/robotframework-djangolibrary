
1.0a6 (unreleased)
------------------

Breaking Changes:

- Change 'Clear DB' implementation to use "python manage.py flush" instead of
  deleting and re-building the database.
  [timo]

- Remove 'Debug' and 'Pause' keywords. The 'Debug' keyword which is
  providedby robotframework-debuglibrary is sufficient.
  [timo]


1.0a5 (2016-02-11)
------------------

- Make middleware part Python 3 compatible.

  robotframework-djangolibrary is still not compatible with Python 3 because
  robotframework-selenium2library does not work with Python 3 yet. Though, you
  can install robotframwork-djangolibrary on Python 3 with "pip install
  robotframework-djangolibrary --no-deps" and then run your tests with
  Python 2.7.
  [timo]

- Add 'Framework :: Robot Framework' classifier to setup.py.
  [timo]


1.0a4 (2016-02-05)
------------------

- Use 'migrate' instead of 'syncdb' for Django > 1.7.x.
  [timo]


1.0a3 (2015-09-28)
------------------

- Add list_classifiers to setup.py.
  [timo]

- Fix user creation and startup. This fixes #3.
  [MatthewWilkes]


1.0a2 (2015-06-25)
------------------

- Remove Django and zest.releaser from requirements.txt. This fixes #2.
  [timo]


1.0a1 (2015-06-24)
------------------

- Initial release.
  [timo]
