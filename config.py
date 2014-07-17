import os

class Config(object):
    DEBUG = False
    MINT_URL = os.environ['MINT_URL']

class DevelopmentConfig(Config):
    DEBUG = True
    CSRF_ENABLED = os.environ['CSRF_ENABLED']
    SECRET_KEY = os.environ['SECRET_KEY']

class TestConfig(DevelopmentConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
