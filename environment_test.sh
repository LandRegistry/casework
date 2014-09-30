# Here we'll create a test database, and override the database to the test values.
set +o errexit
createuser -s casework_frontend_test
createdb -U casework_frontend_test -O casework_frontend_test casework_frontend_test -T template0
set -e

export DATABASE_URL="postgresql://localhost/casework_frontend_test"
export SETTINGS='config.TestConfig'
export MINT_URL='http://0.0.0.0:8001'
export PROPERTY_FRONTEND_URL='http://0.0.0.0:8002'
export SECRET_KEY='local-dev-not-secret'
export CSRF_ENABLED=False
export CASES_URL='http://nowhere'
