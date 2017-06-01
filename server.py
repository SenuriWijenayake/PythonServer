from flask import request, app, jsonify
from flask import Flask
from init import plan_my_trip
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
        rcontent = request.json
        user = request.json['user']
        locations = request.json['locations']
        x = plan_my_trip(user,locations)
        return jsonify(x)
    else:
        return "print: GET LOCATIONS"
