from flask_restful import fields
from my_assist.extensions import db
import datetime

reminder= {
'reminder': fields.String,
'state': fields.String,
'event': fields.String,
'date_created': fields.DateTime,
'date_updated': fields.DateTime
}

class Reminders(db.Document):
    reminder=db.StringField()
    state=db.StringField()
    event=db.StringField()
    date_created=db.CreatedField()
    date_updated=db.ModifiedField()
