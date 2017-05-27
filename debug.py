from pymongo import MongoClient
from crud import *

client = MongoClient('localhost', 27017)
db = client.script

raw_responses = db.new_responses
netSims = list(db.networkSims.find())

all_user = getAllUserIds()
miss_active = []
miss_other = []

for res in list(raw_responses.find()):
    if (str(res['active']) not in all_user):
        miss_active.append(res['active'])
    if (str(res['other']) not in all_user):
        miss_other.append(res['other'])

print ("Missing as active are: ")
print (set(miss_active))

print ("Missing as other are: ")
print (set(miss_other))
