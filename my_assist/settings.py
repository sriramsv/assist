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
    SQLALCHEMY_DATABASE_URI =  "postgres://fukwbmzyejoizc:a40d2f739be06275a24b7416bd57125d356ec981623f7119fe8875f6ef479e4d@ec2-184-73-236-170.compute-1.amazonaws.com:5432/dsbftj344l2it"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    THREADED = True
    SQLALCHEMY_DATABASE_URI = "postgres://fukwbmzyejoizc:a40d2f739be06275a24b7416bd57125d356ec981623f7119fe8875f6ef479e4d@ec2-184-73-236-170.compute-1.amazonaws.com:5432/dsbftj344l2it"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
