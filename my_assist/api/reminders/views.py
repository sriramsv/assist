from flask_restful import marshal_with,Api,Resource,marshal
from .models import reminder,Reminders
from my_assist.extensions import db,states
from flask import Blueprint,request,jsonify,redirect,url_for,abort
import logging,json
from collections import defaultdict
from mongoalchemy.session import Session

logging.basicConfig(level=logging.DEBUG)
blueprint=Blueprint("reminder",__name__)
api=Api(blueprint)
from flask import current_app
class Reminder(Resource):

    @marshal_with(reminder)
    def post(self,state,event):
        data=request.get_json()
        r=Reminders(reminder=data['reminder'].lower(),state=state.lower(),event=event.lower())
        r.save()
        return r

    @marshal_with(reminder)
    def get(self,state,event):
            if event:
                data=Reminders.query.filter(Reminders.state==state.lower(),Reminders.event==event.lower()).all()
            logging.debug(data)
            return data



class ReminderList(Resource):
    @marshal_with(reminder)
    def get(self):
        data=Reminders.query.all()
        return data


class ReminderQuery(Resource):
    @marshal_with(reminder)
    def get(self,qreminder):
        data=Reminders.query.filter(Reminders.reminder==qreminder.lower()).all()
        logging.debug(data)
        return data
    @marshal_with(reminder)
    def delete(self,qreminder):
        f=Reminders.query.filter(Reminders.reminder==qreminder.lower()).first()
        logging.debug(f)
        try:
            f.remove()
        except:
            abort(400)
        return "deleted"
api.add_resource(Reminder,'/reminder/<string:state>/<string:event>')
api.add_resource(ReminderList,'/reminders')
api.add_resource(ReminderQuery,'/reminder/<string:qreminder>')
