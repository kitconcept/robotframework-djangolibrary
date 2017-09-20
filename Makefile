SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DJANGO_VERSION:=1.10.7

all: clean build

clean:
	@echo "Clean"
	rm -rf .py27

build:
	@echo "Build"
	virtualenv .py27 || virtualenv-2.7 .py27
	.py27/bin/pip install -r requirements.txt
	.py27/bin/python setup.py develop
	.py27/bin/pip install . --no-dependencies
	.py27/bin/pip install -q flake8
	.py27/bin/pip install -q psycopg2
	.py27/bin/pip install Django==${DJANGO_VERSION}

test:
	@echo "Run Tests"
	.py27/bin/pybot DjangoLibrary

test-phantomjs:
	@echo "Run Tests"
	.py27/bin/pybot --variable BROWSER:phantomjs DjangoLibrary
