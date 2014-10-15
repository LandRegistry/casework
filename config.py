import os

class Config(object):
    DEBUG = False
    MINT_URL = os.environ['MINT_URL']
    PROPERTY_FRONTEND_URL = os.environ['PROPERTY_FRONTEND_URL']
    CSRF_ENABLED = os.environ['CSRF_ENABLED']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CASES_URL = os.environ['CASES_URL']

    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_PASSWORD_HASH =  os.environ['SECURITY_PASSWORD_HASH']

    # the following two are optional and are only configured on
    # heroku so get safely
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')
    WTF_CSRF_ENABLED=False

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True

