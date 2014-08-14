import os

class Config(object):
    DEBUG = False
    MINT_URL = os.environ.get('MINT_URL')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTY_FRONTEND_URL')
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_PASSWORD_HASH = 'bcrypt'
    # the following two are optional and are only configured on
    # heroku so get safely
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED=True

class TestConfig(DevelopmentConfig):
    TESTING = True

class DockerConfig(Config):
    DEBUG = True
    SECRET_KEY = 'hunter2'
    MINT_URL = os.environ.get('MINT_1_PORT_8001_TCP', '').replace('tcp://', 'http://')
    PROPERTY_FRONTEND_URL = os.environ.get('PROPERTYFRONTEND_1_PORT_8002', '').replace('tcp://', 'http://')
