#!/bin/bash

createuser -s casework_frontend
createdb -U casework_frontend -O casework_frontend casework_frontend -T template0
