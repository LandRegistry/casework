import os

class Config(object):
    DEBUG = False
    MINT_URL = os.environ['MINT_URL']
    CSRF_ENABLED = os.environ['CSRF_ENABLED']
    SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(Config):
    DEBUG = True
    CSRF_ENABLED = False

class TestConfig(DevelopmentConfig):
    TESTING = True

