# Here we'll create a test database, and override the database to the test values.
export APP_NAME="casework_frontend_test"
set +o errexit
createuser -s $APP_NAME
createdb -U $APP_NAME -O $APP_NAME $APP_NAME -T template0
set -e

export DATABASE_URL="postgresql://localhost/$APP_NAME"
export SETTINGS='config.TestConfig'
export MINT_URL='http://0.0.0.0:8001'
export PROPERTY_FRONTEND_URL='http://0.0.0.0:8002'
export SECRET_KEY='local-dev-not-secret'
export CSRF_ENABLED=False
export CASES_URL='http://nowhere'
