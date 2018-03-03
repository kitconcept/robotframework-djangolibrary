SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
DJANGO_VERSION:=1.11.5

all: clean build

clean:
	@echo "Clean"
	rm -rf bin include lib

build:
	@echo "Build"
	virtualenv -p python3 .
	bin/pip install -r requirements.txt
	bin/python setup.py develop
	bin/pip install . --no-dependencies
	bin/pip install -q flake8
	bin/pip install -q psycopg2
	bin/pip install Django==${DJANGO_VERSION}

test:
	@echo "Run Tests"
	bin/pybot DjangoLibrary

