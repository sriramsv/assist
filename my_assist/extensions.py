# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_assistant import Assistant
import os,logging
from my_assist.util.hass import Hass,AppDaemon
from flask import Flask
from flask_mongoalchemy import MongoAlchemy
logging.basicConfig(level=logging.DEBUG)
import wolframalpha

wolfram=wolframalpha.Client(os.getenv("WOLFRAM_ALPHA_KEY"))
db=MongoAlchemy()
homeassistant=Hass(host="jarvispi.duckdns.org",port=443,use_ssl=True,password=os.getenv("HASSPWD"))
appdaemon=AppDaemon(host="jarvispi.duckdns.org",port=443,use_ssl=True)

assist = Assistant()
stateentity=assist.api.get_entity("State")
states=[s["value"].lower() for s in stateentity["entries"]]
logging.debug(states)
