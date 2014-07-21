#!/bin/bash

export SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql://localhost/title_number'
export MINT_URL='http://0.0.0.0:8001'
export PROPERTY_FRONTEND_URL='http://0.0.0.0:8002'
export SECRET_KEY='<F\xab\xdd\x83\xbc\xaa\xcc\xda;1*\x17I\x8d\xf0{\x15\xcd\x89\xaeS$:'
export CSRF_ENABLED=True

createuser -s title_number
createdb -U title_number -O title_number title_number -T template0

python manage.py db upgrade
python run_dev.py

python run_dev.py
