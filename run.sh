#!/bin/bash

source ./environment.sh

set +o errexit
createuser -s casework
createdb -U casework -O casework casework_users -T template0

python manage.py db upgrade
python run_dev.py
