from flask import Flask, url_for, request, jsonify, Response
import sys
sys.path.insert(0,'/home/ubuntu/senuri/PythonServer')
from init import plan_my_trip
from email_classifier import classify_emails

from http.server import BaseHTTPRequestHandler,HTTPServer

app = Flask(__name__)

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo(_self_):
    if request.method == 'POST':
        response = classify_emails()
        return response

    elif request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/locations', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_print(_self_):
    if request.method == 'GET':
        return "print: GET\n"

    elif request.method == 'POST':
        content = request.json
        user = request.json['user']
        locations = request.json['locations']
        x = plan_my_trip(user,locations)
        return jsonify(x)

    elif request.method == 'PATCH':
        return "print: PACTH\n"

    elif request.method == 'PUT':
        return "print: PUT\n"

    elif request.method == 'DELETE':
        return "print: DELETE"

# def run(server_class=HTTPServer, handler_class=S, port=8586):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print ('Starting httpd...')
#     httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    app.run(host='0.0.0.0', debug=False)


