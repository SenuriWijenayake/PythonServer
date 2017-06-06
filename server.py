from flask import request, app, jsonify
from flask import Flask
from startup import *
from rate_locations_script import rate_these_locations
from locationClassifier import classifyLocations
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
        content = request.json
        user = request.json['user']
        locations = request.json['locations']
        x = rate_these_locations(user,locations,avgs,all_sims)
        return jsonify(x)
    else:
        return "print: GET LOCATIONS"
