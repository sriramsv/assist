# -*- coding: utf-8 -*-
""" Reminder section """
from flask import Blueprint,jsonify,request
import requests,json
from .models import statereminder
from my_assist.extensions import manager
from models import db

blueprint=manager.create_api_blueprint('statereminder',statereminder,methods=['GET','POST','PATCH','DELETE'])
