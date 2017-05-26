from pymongo import MongoClient
from crud import *

client = MongoClient('localhost', 27017)
db = client.script

raw_responses = db.responses_raw.find()
responses = db.responses

def findResponsesOfUser (active):
    res = db.responses_raw.find({'active':int(active)})
    my_resposes = {}
    for response in list(res):
        res = {'1' : int(response['Q1']),
               '2' : int(response['Q2']),
               '3' : int(response['Q3']),
               '4' : int(response['Q4'])
               }
        my_resposes[str(response['other'])] = res
    responses.insert({'id': active, 'responses' : my_resposes })

all_users = getAllUsers()
for user in list(all_users):
    findResponsesOfUser(user['id'])

