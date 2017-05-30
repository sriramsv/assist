# -*- coding: utf-8 -*-

# my_assist
# By sriramsv <sriramsv007@gmail.com>
#
# A Virtual Assistant created with flask and flask-assistant

import logging
from flask import Blueprint,url_for,redirect
from flask_assistant import Assistant, ask, tell,intent,context_manager
import requests,os,simplejson
from my_assist.util.helper import get_template

blueprint = Blueprint('assist', __name__, url_prefix='/assist')
assist = Assistant(blueprint=blueprint)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

port = os.getenv("PORT")
base_url = "http://0.0.0.0:"+port
@assist.action('Greetings')
def welcome():
    speech = 'Welcome, to my_assist!'
    return ask(speech)

@assist.action('train')
def train(state):
    r=requests.get(base_url+url_for('public.train',state=state))
    return tell(r.text)

@assist.action('setstatereminder')
def setstatereminder(reminder,state,event):
    data,headers=get_template("statereminder",{"reminder":reminder,"state":state,"event":event})
    r=requests.post(base_url+"/api/statereminder",headers=headers, data=simplejson.dumps(data))
    return tell("Ok, will remind you to {} when you {} {}".format(reminder,event,state))

@assist.action('getstatereminder')
def getstatereminder(state,event):
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    if not event:
        filters = [dict(name='state', op='eq', val=state.title())]
    else:
        filters = [dict(name='state', op='eq', val=state.title()),dict(name='event', op='eq', val=event.title())]
    params = {'filter[objects]': simplejson.dumps(filters)}
    r = requests.get(base_url+"/api/statereminder", params=params, headers=headers)
    if r.status_code!=200:
        return tell("I seem to have trouble getting the data")
    data=r.json()
    sdata=data['data']
    ret=[]
    if len(sdata)==0:
        if not event:
            return tell("No reminders for {}".format(state))
        else:
            return tell("No reminders for {} {}".format(state,event))
    for s in sdata:
        ret.append(s["attributes"]["reminder"])
    return tell("You have the following reminders for {}:".format(state)+ ",".join(ret))

@assist.action('deletestatereminder')
def deletestatereminder(state,event):
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    if not event:
        filters = [dict(name='state', op='eq', val=state.title())]
    else:
        filters = [dict(name='state', op='eq', val=state.title()),dict(name='event', op='eq', val=event.title())]
    params = {'filter[objects]': simplejson.dumps(filters)}
    r = requests.get(base_url+"/api/statereminder", params=params, headers=headers)
    if r.status_code!=200:
        return tell("I seem to have trouble getting the data")
    data=r.json()
    sdata=data['data']
    ret=[]
    links=[]
    if len(sdata)==0:
        if not event:
            return tell("No reminders for {}".format(state))
        else:
            return tell("No reminders for {} {}".format(state,event))
    for i,s in enumerate(sdata):
        ret.append(s["attributes"]["reminder"])
        links.append(s["links"]["self"])
    context_manager.set('deletestatereminder-followup', 'reminders',links)
    speech="You have the following reminders:\n"
    speech+=",".join(ret)+"\n"
    speech+="which one do you want to delete?"
    return ask(speech)


@assist.context('deletestatereminder-followup')
@assist.action('select-delete-rem')
def deleteselected(number,links):
    headers={"Accept":"application/vnd.api+json","Content-Type": "application/vnd.api+json"}
    l=[];speech=""
    if len(number)>len(links):
        return ask("You just have {} reminders to choose from, please choose the correct number".format(len(links)))
    for i in number:
            l.append(links[i-1])

    def delete_rem(link):
        r=requests.delete(link,headers=headers)
        return r.status_code
    for rem in l:
        code=delete_rem(rem)
        if code!=204:
            speech+="Could not delete {}".format(rem)
        speech+="Deleted successfully"
    return tell(speech)
