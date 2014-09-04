#!/bin/bash
# This script runs the app on the preview environment.
#
# NOTE: It does not upgrade the database. As there may be multiple nodes deployed 
# on these environments we do not run the database migrations automatically. It is 
# expected that the environment deployment scripts will do this before deploying the
# new apps.

set -e

python run_dev.py
