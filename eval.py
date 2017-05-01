from pymongo import MongoClient
from crud import *

client = MongoClient('localhost', 27017)
db = client.script

#Function to get the existing locations for a given user
def get_existing_locs(user,data):
    user_prefs = data[user]
    locations = []
    for key in user_prefs.items():
        #Check if in preferences of other users
        if(not isNewLocation(key)):
            locations.append(key)
    print (locations)


#Function to calcualte the root mean square error
def root_mean_sqaure(actual,expected):
