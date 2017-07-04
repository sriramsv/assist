# -*- coding: utf-8 -*-
"""Application configuration.

See https://github.com/sloria/cookiecutter-flask for configuration options with other flask-extensions
"""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('MY_ASSIST_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    MONGOALCHEMY_CONNECTION_STRING="mongodb://apiaihandler:apiai@ds147979.mlab.com:47979/heroku_jtsbsf80"
    MONGOALCHEMY_DATABASE="heroku_jtsbsf80"

class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    THREADED = True
    MONGOALCHEMY_CONNECTION_STRING="mongodb://apiaihandler:apiai@ds147979.mlab.com:47979/heroku_jtsbsf80"

class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
