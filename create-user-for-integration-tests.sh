#!/bin/bash

USER_EMAIL="caseworker@example.org"
USER_PASSWORD="dummypassword"

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "casework-frontend"
python manage.py create_user --email=${USER_EMAIL} --password=${USER_PASSWORD}
deactivate

echo
echo
echo "Created user: ${USER_EMAIL} with password: ${USER_PASSWORD}"
echo
echo
