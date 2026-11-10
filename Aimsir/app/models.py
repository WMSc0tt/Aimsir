from datetime import datetime
from app import db

#we need to create a user table model
class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# create the sightings table model
class Sighting(db.Model):
    __tablename__ = 'sightings'
    sighting_id = db.Column(db.String(50), primary_key=True, nullable=False)
    s_datetime = db.Column(db.String(50))
    s_city = db.Column(db.String(30))
    s_weather_type = db.Column(db.String(255))
    summary = db.Column(db.String(255))
    userid = db.Column(db.String(50), db.ForeignKey('users.userid'))