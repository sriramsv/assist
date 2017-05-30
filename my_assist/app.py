# -*- coding: utf-8 -*-
"""The flask app module, containing the app factory function."""
from flask import Flask, render_template

from my_assist import assistant, web,reminder
from my_assist.extensions import assist,db,manager
from flask_restless import APIManager
from my_assist.settings import ProdConfig
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions.

    Flask-Assistant does not need to be initalized here if declared as a blueprint.
    Other extensions such as flask-sqlalchemy and flask-migrate are reigstered here.
    If the entire flask app consists of only the Assistant, uncomment the code below.
    """
    # assist.init_app(app, route='/')
    # db.create_all()
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
    manager.init_app(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints.

    When Flask-Assistant is used to create a blueprint within a standard flask app,
    it must be registered as such, rather that with init_app().

    If the entire flask app consists of only the Assistant, comment out the code below.
    """
    app.register_blueprint(assistant.webhook.blueprint)
    app.register_blueprint(web.views.blueprint)
    # app.register_blueprint(manager.create_api_blueprint(reminder.models.Reminder,methods=["GET","POST"]))
    app.register_blueprint(reminder.views.blueprint)

    app.logger.info(app.url_map)


    return None
