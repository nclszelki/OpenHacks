# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask import request, redirect
# from app import db
import pymongo

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def index():


    #here we can save the items to an array from the database and then loop through in the index2 template


    return render_template('home/index2.html')

@blueprint.route('/', methods = ['POST'])
def addItem():
    item = {
        "itemName" : request.form['name'],
        "description" : request.form['description'],
        "imageLink" : request.form['image_link']
    }
    
    # itemsCollection = db.items
    # items.insert_one(item)

    
    return render_template('/home/index2.html')