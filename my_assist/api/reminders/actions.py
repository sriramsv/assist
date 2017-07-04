from my_assist.extensions import assist
from flask_assistant import tell
import requests
from flask import url_for
import json

@assist.action('setstatereminder')
def setstatereminder(reminder,state,event):
    headers={"Content-Type":"application/json"}
    data={"reminder":reminder}
    r=requests.post(url_for("reminder.reminder",state=state,event=event,_external=True),data=json.dumps(data),headers=headers)
    if r.status_code!=200:
        return tell("Something went wrong, please try again later")
    return tell("Ok added your reminder")


@assist.action("getstatereminder")
def getreminder(state,event):
    r=requests.get(url_for("reminder.reminder",state=state,event=event,_external=True))
    if r.status_code!=200:
        return tell("Could not fetch state reminders at this point in time")
    speech=[]
    data=r.json()
    if len(data)==0:
        return tell("no reminders currently for {} {}".format(state,event))
    for d in data:
        speech.append(d['reminder'])
    return tell("you have the following reminders: {}".format(",".join(speech)))