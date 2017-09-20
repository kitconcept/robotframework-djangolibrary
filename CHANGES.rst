
2.0 (2017-09-20)
----------------

Breaking Changes:

- Remove deprecated method from internal startup flow.
  [cdvv7788]

New Features:

- Use AUTH_MODEL to create user instead of django's default
  [cdvv7788]

- Upgrade FactoryBoy to version 2.8.1
  [amarandon]

- Add Django 1.10.7 and 1.11.1 support.
  [timo]

- LICENSE.txt added.
  [timo]

Bugfixes / Minor Changes:

- Move tests to use Chrome.
  [timo]

- Upgrade tests to Django 1.11.5, 1.10.8, 1.9.13, 1.8.18.
  [timo]

- Add Django 1.11 and 1.10 to setup.py.
  [timo]


1.2 (2016-07-08)
----------------

New Features:

- Make Factory Boy keyword return 'pk' attribute.
  [timo]


1.1 (2016-07-07)
----------------

New Features:

- Add QuerySet keyword.
  [timo]

- Make it possible to override subfactories when using the `FactoryBoy`
  keyword.
  [timo]

Bugfixes:

- Use Django's model_to_dict method to serialize the response objects for the
  factory_boy keyword.
  [timo]


1.0 (2016-06-30)
----------------

- Re-release 1.0a6 as 1.0.
  [timo]


1.0a6 (2016-04-29)
------------------

New Features:

- Python 3 compatibility. Note that the latest offical release of
  robotframework-selenium2library is currently not compatible with Python 3.
  See https://github.com/HelioGuilherme66/robotframework-selenium2library/releases for a working pre-release and details.
  [timo]

- Support for Postgres added. All Django database backends should work.
  We test SQLite and Postgres only though.
  [timo]

- Add 'Factory Boy' keyword. This allows us to use factory_boy factories in
  Robot Framework tests.
  [timo]

Breaking Changes:

- Drop Django 1.7.x support. We test and support Django 1.8.x and 1.9.x.
  [timo]

- Change 'Clear DB' implementation to use "python manage.py flush" instead of
  deleting and re-building the database.
  [timo]

- Remove 'Debug' and 'Pause' keywords. The 'Debug' keyword, which is
  provided by robotframework-debuglibrary is sufficient.
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
