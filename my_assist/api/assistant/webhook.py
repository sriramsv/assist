# -*- coding: utf-8 -*-

# my_assist
# By sriramsv <sriramsv007@gmail.com>
#
# A Virtual Assistant created with flask and flask-assistant

import logging
from flask import Blueprint,url_for,redirect
from flask_assistant import Assistant, ask, tell,intent,context_manager
import requests,os,json
from my_assist.util.helper import get_template
from my_assist.extensions import assist
blueprint = Blueprint('assist', __name__, url_prefix='/assist')
assist.init_blueprint(blueprint)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)


@assist.action('Greetings')
def welcome():
    speech = 'Welcome, to my_assist!'
    return ask(speech)

@assist.action('train')
def train(state):
    r=requests.get(base_url+url_for('public.train',state=state))
    return tell(r.text)

@assist.action("garagestatus")
def gstatus():
    r=requests.get("https://jarvispi.duckdns.org/api/states/cover.garage?api_password="+os.getenv("HASSPWD"))
    if r.status_code!=200:
        return tell("Sorry,something went wrong,try again whenever you are ready")
    return tell("Garage is currently %s" % r.json()['state'])
