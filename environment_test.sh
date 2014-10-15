export SETTINGS='config.TestConfig'
# Here we'll create a test database, and override the database to the test values.
set +o errexit
createuser -s casework_frontend_test
createdb -U casework_frontend_test -O casework_frontend_test casework_frontend_test -T template0
set -e

export DATABASE_URL="postgresql://localhost/casework_frontend_test"
export MINT_URL='http://nowhere'
export PROPERTY_FRONTEND_URL='http://nowhere'
export CASES_URL='http://nowhere'
export CSRF_ENABLED=False
export SECRET_KEY='localdev-not-secret'
export SECURITY_PASSWORD_HASH='bcrypt'
