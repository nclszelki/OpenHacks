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
        return redirect(url_for('home.index'))

    return render_template('am.html')

@blueprint.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home.index'))

    return "Incorrect Username/Password!"

@blueprint.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.clear()
        return "User Logged Out"

@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('home.index'))
        
        return 'Account exists'

    return render_template('amregister.html')
