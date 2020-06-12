#!/usr/bin/env bash

set -e
coverage run manage.py test && flake8
coverage report
coveralls --rcfile=.coveragerc
ls