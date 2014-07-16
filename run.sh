#!/bin/bash

export SETTINGS='config.DevelopmentConfig'
export MINT_URL='http://0.0.0.0:8001'
export SECRET_KEY="<F\xab\xdd\x83\xbc\xaa\xcc\xda;1*\x17I\x8d\xf0{\x15\xcd\x89\xaeS$:"
export CSRF_ENABLED=True

python run_dev.py
