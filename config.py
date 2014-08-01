import os

class Config(object):
    DEBUG = False
    MINT_URL = os.environ['MINT_URL']
    CSRF_ENABLED = os.environ['CSRF_ENABLED']
    SECRET_KEY = os.environ['SECRET_KEY']
    PROPERTY_FRONTEND_URL = os.environ['PROPERTY_FRONTEND_URL']
    # the following two are optional and are only configured on
    # heroku so get safely
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True

class DockerConfig(Config):
    DEBUG = True
    SECRET_KEY = 'hunter2'
    MINT_URL = os.environ.get('MINT_1_PORT_8001_TCP', '').replace('tcp://', 'http://')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTYFRONTEND_1_PORT_8002', '').replace('tcp://', 'http://')
