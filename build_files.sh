#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/

