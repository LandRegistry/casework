#!/bin/bash


./db/upgrade-database.sh
python run_dev.py
