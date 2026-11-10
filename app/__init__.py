#this file if fro the applications main points in its flask 
#import the flask and config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

#create an app variable to avbe able to be use to store the name passed from teh flak class
app = Flask(__name__)

#read and apply the confic keys
app.config.from_object(Config)

#import the database instance for the sql
db = SQLAlchemy(app)
#import the routes and models to be able to use them in the app
from app import routes, models