  
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask import request, redirect
# from app import db
import pymongo
from pymongo import MongoClient

blueprint = Blueprint('home', __name__)

client = pymongo.MongoClient("mongodb://penguin022:Ji0G552V7QT83xCr@cluster0-shard-00-00-yinp0.azure.mongodb.net:27017,cluster0-shard-00-01-yinp0.azure.mongodb.net:27017,cluster0-shard-00-02-yinp0.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

@blueprint.route('/')
def index():


    #here we can save the items to an array from the database and then loop through in the index2 template
    items = db.items

    return render_template('home/index2.html', items = items)

@blueprint.route('/', methods = ['POST'])
def addItem():
    item = {
        "itemName" : request.form['name'],
        "description" : request.form['description'],
        "location" : request.form['location'],
        "imageLink" : request.form['image_link']
    }
    
    items= db.items
    items.insert_one(item)

    
    return render_template('/home/index2.html', items = items)