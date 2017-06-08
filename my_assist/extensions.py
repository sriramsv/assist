# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_assistant import Assistant
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
import os
from redis import StrictRedis as Redis


redisurl=os.getenv("REDISTOGO_URL")
db = SQLAlchemy()
assist = Assistant()
cache=Redis.from_url(redisurl)
manager=APIManager(flask_sqlalchemy_db=db)
