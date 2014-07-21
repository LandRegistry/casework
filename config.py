import os

class Config(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MINT_URL = os.environ.get('MINT_URL')
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED')
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
    MINT_URL = 'http://locahost:8005'
