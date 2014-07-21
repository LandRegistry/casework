import os

class Config(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MINT_URL = os.environ.get('MINT_URL')
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTY_FRONTEND_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
    MINT_URL = 'http://locahost:8005'
    PROPERTY_FRONTEND_URL = 'http://localhost:8002'
