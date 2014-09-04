#!/bin/bash

echo "Creating database for casework-frontend"

createuser -s casework
createdb -U casework -O casework casework_users -T template0
