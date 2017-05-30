# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_assistant import Assistant
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
db = SQLAlchemy()
assist = Assistant()
manager=APIManager(flask_sqlalchemy_db=db)
