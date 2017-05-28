# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
import requests,json
blueprint = Blueprint('public', __name__, static_folder='../static')
from my_assist.lib import db as database

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Landing page for the web/html blueprint"""
    return "my_assist Web Page"

@blueprint.route("/train/<state>",methods=["GET"])
def train(state):
    db=database.DB()
    key=db.get("Maps_API_Key")
    state=state.title()
    if state=="Work":
        src=db.get("Home_Station")
        dest=db.get("Work_Station")
    elif state=="Home":
        src=db.get("Work_Station")
        dest=db.get("Home_Station")
    else:
        return "This function is only for Home and Work,specify correct state"

    url="https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}&mode=transit".format(src,dest,key)
    r=requests.get(url)
    if r.status_code!=200:
        return "Cannot fetch train details right now"
    body=json.loads(r.text)
    timing=body["routes"][0]["legs"][0]["steps"][1]["transit_details"]["departure_time"]["text"]
    return timing
