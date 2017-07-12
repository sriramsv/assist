# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, session, redirect, request,jsonify
import requests,json,os,logging
import my_assist.util
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from flask_assistant import tell
from my_assist.extensions import assist
logging.basicConfig(level=logging.debug)

consumer_key = os.getenv('SPLITWISE_CONSUMER_KEY')
consumer_secret = os.getenv('SPLITWISE_CONSUMER_SECRET')
blueprint = Blueprint('splitwise',__name__,url_prefix="/splitwise")

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    if 'access_token' in session:
    	return redirect(url_for("splitwise.friends"))
    sObj = Splitwise(consumer_key,consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    with open('secret','w') as f:
    	f.write(secret)
    session.permanent = True
    logging.info("Redirecting to url {}".format(url))
    return redirect(url)

@blueprint.route("/authorize",methods=["GET"])
def authorize():
    secret = ""
    with open('secret','r') as f:
    	secret = f.readline()
    	secret = secret.strip()

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    logging.info(oauth_token,oauth_verifier)
    sObj = Splitwise(consumer_key,consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,secret,oauth_verifier)
    logging.info(access_token)
    with open('accesstoken.json','w') as f:
    	json.dump(access_token,f)
    session['access_token'] = access_token
    return redirect(url_for("splitwise.groups"))

@blueprint.route("/friends",methods=["GET"])
def friends():
    global consumer_key,consumer_secret
    if 'access_token' not in session:
        return redirect(url_for("splitwise.home"))
    access_token = 0
    with open('accesstoken.json','r') as f:
        access_token = json.load(f)
    sObj = Splitwise(consumer_key,consumer_secret)
    sObj.setAccessToken(access_token)
    logging.info(sObj.getFriends())
    friends=[{f.getFirstName():[x.getAmount() for x in f.getBalances()]} for f in sObj.getFriends()]
    return jsonify(friends)

@blueprint.route("/groups",methods=["GET"])
def groups():
    global consumer_key,consumer_secret
    if 'access_token' not in session:
        return redirect(url_for("splitwise.home"))
    access_token = 0
    with open('accesstoken.json','r') as f:
        access_token = json.load(f)
    sObj = Splitwise(consumer_key,consumer_secret)
    sObj.setAccessToken(access_token)
    logging.info(sObj.getFriends())
    friends=[f.getName() for f in sObj.getGroups()]
    return jsonify(friends)

@assist.action("friend")
def addMoney(friendName, currency, expenseReason):
	speech = "hello"
	print "name =", friendName
	print currency
	print "inside add money"
	if not friendName or not currency:
		print "error in name or currency"
		return tell("sorry couldn't proceed with transaction")


	consumer_key = 'CONSUMER_KEY'
	consumer_secret = 'CONSUMER_SECRET'
	sObj = Splitwise(consumer_key,consumer_secret)

	with open('accesstoken.json','r') as f:
		access_token = json.load(f)
		print access_token
	sObj.setAccessToken(access_token)


	amountOwed = currency['amount']
	expense = Expense()
	expense.setCost(amountOwed)
	expense.setDescription(expenseReason)

	user1 = ExpenseUser()
	user1.setId(utils.getSplitwiseId('nirmit'))
	user1.setPaidShare(str(amountOwed))
	user1.setOwedShare('0.0')

	user2 = ExpenseUser()
	user2.setId(utils.getSplitwiseId(friendName))
	user2.setPaidShare('0.00')
	user2.setOwedShare(str(amountOwed))

	users = []
	users.append(user1)
	users.append(user2)
	expense.setUsers(users)

	expense = sObj.createExpense(expense)
	print expense
