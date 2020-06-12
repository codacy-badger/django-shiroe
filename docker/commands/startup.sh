#!/usr/bin/env bash

set -e
python3 manage.py wait_for_db
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:8000