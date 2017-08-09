# -*- coding: utf-8 -*-

# my_assist
# By sriramsv <sriramsv007@gmail.com>
#
# A Virtual Assistant created with flask and flask-assistant

import logging
from flask import Blueprint,url_for,redirect,request
from flask_assistant import Assistant, ask, tell,intent,context_manager
import requests,os,json,datetime,parsedatetime
from my_assist.util.helper import get_template,calc_delay
from my_assist.extensions import assist,homeassistant,wolfram
from flask_assistant import ApiAi
from api_ai.models import Entity
import itertools


blueprint = Blueprint('assist', __name__, url_prefix='/assist')
assist.init_blueprint(blueprint)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

ne=homeassistant.get_entities()

a=ApiAi()
e=Entity("HassEntities")
logging.info(len(ne))
for k,v in ne.items():
    e.add_entry(k,list(v))

entitieslist=[str(s) for s in a.agent_entities]
logging.debug(entitieslist)
if str(e) in entitieslist:
    a.put_entity(e.name,e.serialize)
else:
    a.post_entity(e.serialize)

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
def gstatus(entity_id):
    device=entity_id
    gstate=homeassistant.get_state(entity_id=device)
    if not gstate:
        return tell("Something went wrong, try again whenever you are ready")
    logging.debug(gstate)
    state=gstate.state
    friendly_name=gstate.attributes['friendly_name']
    return tell("The {} is now {}".format(friendly_name,state))


@assist.action("lateraction")
def lateraction(entity_id,delay,switch):
    delay=calc_delay(delay)
    service=homeassistant.get_services_for_entity(entity_id,switch)
    data={"service":service,"delay":delay,"entity_id":entity_id}
    s=homeassistant.fire_event("schedule",data)
    return tell("ok scheduled")

@assist.action("scheduleaction")
def scheduleaction(entity_id,switch):
    service=homeassistant.get_services_for_entity(entity_id,switch)
    logging.debug("Service:{}".format(service))
    x=homeassistant.call_service(domain=service.split("/")[0],service=service.split("/")[1],entity_id=entity_id)
    if not x:
        return tell("Could not call service {}".format(service))
    return "Done!"

@assist.action("laterevent")
def laterevent(entity_id,state,event,switch):
    service=homeassistant.get_services_for_entity(entity=entity_id,switch=switch)
    data={"service":service,"state":state,"event":event,"entity_id":entity_id}
    s=homeassistant.fire_event("stateschedule",data)
    return tell("ok scheduled action on {} {}".format(state,event))
