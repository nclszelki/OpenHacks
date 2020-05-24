from flask import Flask, render_template, url_for, request, session, redirect, Blueprint
import pymongo
from pymongo import MongoClient
import bcrypt


client = pymongo.MongoClient("mongodb://penguin022:Ji0G552V7QT83xCr@cluster0-shard-00-00-yinp0.azure.mongodb.net:27017,cluster0-shard-00-01-yinp0.azure.mongodb.net:27017,cluster0-shard-00-02-yinp0.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

blueprint = Blueprint('account', __name__, url_prefix='/account')

@blueprint.route('/')
def index():
    if 'username' in session:
        return "<center>User Already Logged In</center> <center> <a href='/'> Click to go back to Home Page</a> </center>"

    return render_template('am.html')

@blueprint.route('/login', methods=['POST'])
def login():
    
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home.index'))

    return "<center>Incorrect Username/Password!<center> <center> <a href='/'> Click to go back to Home Page</a> </center>"

@blueprint.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        username = session['username']
        session.clear()
        return "<center> User Logged Out: " + username + "</center>" + "<center> <a href='/' Click to go back to home page> Home Page </a> </center>"
    else:
        return "<center> No User Logged In </center> <center> <a href='/'> Click to go back to Home Page</a> </center>"

@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return "<center> Registration Successful! <center> <center> <a href='/'> Click to go back to Home Page</a> </center>"
        
        return "<center> Account Already Exists <center> <center> <a href='/'> Click to go back to Home Page</a> </center>"

    return render_template('amregister.html')
