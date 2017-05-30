import datetime

from my_assist.extensions import db

class statereminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.Unicode)
    state=db.Column(db.Unicode)
    event=db.Column(db.Unicode)
