from flask_restful import marshal_with,Api,Resource,marshal
from models import reminder,Reminders
from my_assist.extensions import db
from flask import Blueprint,request,jsonify,redirect,url_for
import logging,json

logging.basicConfig(level=logging.DEBUG)
blueprint=Blueprint("reminder",__name__)
api=Api(blueprint)

class Reminder(Resource):

    @marshal_with(reminder)
    def post(self,state=None,event=None):
        data=request.get_json()
        logging.debug(data)
        r=Reminders(reminder=data['reminder'],state=state.lower(),event=event.lower())
        r.save()
        return r

    @marshal_with(reminder)
    def get(self,state,event):
        state=state.lower()
        event=event.lower()
        data=Reminders.query.filter(Reminders.state==state and Reminders.event==event).all()
        logging.debug(data)
        return data

    @marshal_with(reminder)
    def delete(self,state,event):
        state=state.lower()
        event=event.lower()
        rem=request.get_json()['reminder']
        f=Reminders.query.filter(Reminders.reminder==rem and Reminders.state==state and Reminders.event==event).first()
        logging.debug(f)
        f.remove()
        redirect(url_for("reminder.reminderlist"))

class ReminderList(Resource):
    @marshal_with(reminder)
    def get(self):
        data=Reminders.query.all()
        logging.debug(data)
        return data

api.add_resource(Reminder,'/reminder/<string:state>/<string:event>')
api.add_resource(ReminderList,'/reminders')
