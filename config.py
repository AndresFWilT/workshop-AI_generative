import os

class Config(object):
    SECRET_KEY = 'ia-generativa'
    UPLOAD_FOLDER = 'static\images'

class DevelopmentConfig(Config):
    DEBUG = True