#!/bin/bash

createuser -s casework
createdb -U casework -O casework casework_users -T template0
