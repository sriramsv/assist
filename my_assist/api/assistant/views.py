# -*- coding: utf-8 -*-

# my_assist
# By sriramsv <sriramsv007@gmail.com>
#
# A Virtual Assistant created with flask and flask-assistant

import logging
from flask import Blueprint,url_for,redirect,request
from flask_assistant import Assistant, ask, tell,intent,context_manager
import requests,os,json,datetime,parsedatetime
from my_assist.util.helper import get_template
from my_assist.extensions import assist,homeassistant,wolfram

blueprint = Blueprint('assist', __name__, url_prefix='/assist')
assist.init_blueprint(blueprint)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)




@assist.action("Default Fallback Intent")
def default():
    query =  request.get_json()['result']['resolvedQuery']
    r=wolfram.query(query)
    res=next(r.results).text
    return tell(res)

@assist.action('train')
def train(state):
    r=requests.get(url_for('public.train',state=state,_external=True))
    return tell(r.text)

@assist.action("devicestatus")
def gstatus(device):
    gstate=homeassistant.get_state(entity_id=device)
    if not gstate:
        return tell("Something went wrong, try again whenever you are ready")
    logging.debug(gstate)
    state=gstate.state
    friendly_name=gstate.attributes['friendly_name']
    return tell("The {} is now {}".format(friendly_name,state))


@assist.action("lateraction")
def lateraction(entity_id,delay,switch):
    service=homeassistant.get_services_for_entity(entity=entity_id,switch=switch)
    cal = parsedatetime.Calendar()
    delaytime,ok=cal.parse(delay)
    delaytime=datetime.datetime(*delaytime[:6])-datetime.datetime.now()
    logging.debug(delaytime)
    seconds=abs(delaytime.total_seconds())
    data={"service":service,"delay":seconds,"entity_id":entity_id}
    s=homeassistant.fire_event("schedule",data)
    return tell("ok scheduled")


@assist.action("laterevent")
def laterevent(entity_id,state,event,switch):
    service=homeassistant.get_services_for_entity(entity=entity_id,switch=switch)
    data={"service":service,"state":state,"event":event,"entity_id":entity_id}
    s=homeassistant.fire_event("stateschedule",data)
    return tell("ok scheduled action on {} {}".format(state,event))
