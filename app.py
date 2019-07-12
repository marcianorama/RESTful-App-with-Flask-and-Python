from flask import Flask, request, session, redirect, render_template, url_for
from flask_pymongo import pymongo
import logging as logger

appInstance = Flask(__name__)

#appInstance.config()
#appInstance.config(mongorestore --host UrbanPiper-shard-0/urbanpiper-shard-00-00-mckcy.mongodb.net:27017,urbanpiper-shard-00-01-mckcy.mongodb.net:27017,urbanpiper-shard-00-02-mckcy.mongodb.net:27017 --ssl --username shivenpurohit --password <PASSWORD> --authenticationDatabase admin )
appInstance.secret_key = "abc"

mongo = pymongo.MongoClient("mongodb+srv://shivenpurohit:microsoft12#@urbanpiper-mckcy.mongodb.net/test?retryWrites=true&w=majority")


##### Auth code #####
@appInstance.route('/index')
def index():
    print(session)
    if ('username' in session):
        return "You're logged in as " + session['username']
    return render_template("index.html")

@appInstance.route('/login', methods=['POST'])
def login():
    print(session)
    users = mongo.db.Users
    login_user = users.find_one({'username':request.form['username']})

    if(login_user is not None):
        if(login_user['password'] == request.form['pass']):
            session['username'] = request.form['username']
            session['role'] = login_user['role']
            return 'You\'re logged in as '+session['username']
        return "invalid username/password"
    return "user doesn't exist"

@appInstance.route('/logout', methods=['GET'])
def logout():
   # remove the username from the session if it is there
    if('username' in session):
       session.pop('username', None)
    return redirect(url_for('index'))

@appInstance.route('/register', methods=['POST', 'GET'])
def register():
    if(request.method == 'POST'):
        users = mongo.db.Users
        existing_user = users.find_one({'username':request.form['username']})

        if(existing_user is None):
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            hashpass = request.form['pass']
            users.insert({'username':request.form['username'], 'password':hashpass, 'role':request.form['role']})
            session['username'] = request.form['username']
            session['role'] = request.form['role']
            return redirect(url_for('index'))

        return 'This username already exists'

    return render_template("index.html")


if(__name__ == '__main__'):
    logger.debug("Starting the application")
    from api import *
    appInstance.run(host="127.10.10.10", port=5000, debug=True, use_reloader=True)

