# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_assistant import Assistant
import os
from util.hass import Hass
from flask import Flask
from flask_mongoalchemy import MongoAlchemy
db=MongoAlchemy()
homeassistant=Hass(host="jarvispi.duckdns.org",port=443,use_ssl=True,password=os.getenv("HASSPWD"))
assist = Assistant()
