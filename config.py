import os

class Config(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'a very secret thing indeed TODO: Get this from the os.environ - i.e. generate and export one'
    MINT_URL = os.environ['MINT_URL']

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

