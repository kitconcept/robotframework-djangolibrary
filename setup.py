from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='robotframework-djangolibrary',
      version=version,
      description="A robot framework library for Django.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='robotframework django test',
      author='Timo Stollenwerk',
      author_email='tisto@plone.org',
      url='http://timostollenwerk.net',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
