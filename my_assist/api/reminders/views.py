from flask_restful import marshal_with,Api,Resource,marshal
from .models import reminder,Reminders
from my_assist.extensions import db
from flask import Blueprint,request,jsonify,redirect,url_for
import logging,json

logging.basicConfig(level=logging.DEBUG)
blueprint=Blueprint("reminder",__name__)
api=Api(blueprint)

class Reminder(Resource):

    @marshal_with(reminder)
    def post(self,state,event):
        logging.debug(request.headers["Content-Type"])
        logging.debug("json",request.get_json())
        data=request.get_json()
        r=Reminders(reminder=data['reminder'],state=state.lower(),event=event.lower())
        r.save()
        return r

    @marshal_with(reminder)
    def get(self,state,event):
        data=Reminders.query.filter(Reminders.state==state.lower() and Reminders.event==event.lower()).all()
        logging.debug(data)
        return data

    @marshal_with(reminder)
    def delete(self,state,event):
        rem=request.get_json()['reminder']
        f=Reminders.query.filter(Reminders.reminder==rem and Reminders.state==state.lower() and Reminders.event==event.lower()).first()
        logging.debug(f)
        f.remove()
        return "deleted"

class ReminderList(Resource):
    @marshal_with(reminder)
    def get(self):
        data=Reminders.query.all()
        logging.debug(data)
        return data

api.add_resource(Reminder,'/reminder/<string:state>/<string:event>')
api.add_resource(ReminderList,'/reminders')
