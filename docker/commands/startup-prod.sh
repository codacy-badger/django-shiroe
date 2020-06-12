#!/usr/bin/env bash

set -e
python3 manage.py wait_for_db
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
/usr/local/bin/gunicorn django_shiroe.wsgi:application -w 2 -b :8000