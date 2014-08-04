#!/bin/bash

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "casework-frontend"
python manage.py create_user --email=caseworker@example.org --password=dummypassword

deactivate
