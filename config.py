import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MINT_URL = os.environ.get('MINT_URL')
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTY_FRONTEND_URL')
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True
    MINT_URL = 'http://locahost:8005'

class TestConfig(DevelopmentConfig):
    TESTING = True
    MINT_URL = 'http://locahost:8005'
    PROPERTY_FRONTEND_URL = 'http://localhost:8002'

class DockerConfig(Config):
    DEBUG = True
    SECRET_KEY = 'hunter2'
    MINT_URL = os.environ.get('MINT_1_PORT_8001_TCP', '').replace('tcp://', 'http://')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTYFRONTEND_1_PORT_8002', '').replace('tcp://', 'http://')
