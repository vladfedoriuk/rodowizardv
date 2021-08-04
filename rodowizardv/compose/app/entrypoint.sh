#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py migrate --noinput

python manage.py initadmin

python manage.py inittokens

python manage.py runserver 0.0.0.0:9071