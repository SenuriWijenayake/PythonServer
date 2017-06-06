from flask import request, app, jsonify
from flask import Flask
from startup import *
from gis import get_rated_locations
from email_classifier import classify_emails
app = Flask(__name__)


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        response = classify_emails()
        return response
    else:
       return "print: GET"


@app.route('/locations', methods=['GET','POST'])
def location():
    if request.method == 'POST':
        user = request.json['user']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        hours = request.json['hours']
        radius = request.json['radius']
        x = get_rated_locations(user,latitude,longitude,hours,radius,training_data,avgs,all_sims,location_train_set)
        return jsonify(x)
    else:
        return "print: GET LOCATIONS"
