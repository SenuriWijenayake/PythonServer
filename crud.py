#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
preferences = db.preferences

#Function to retreieve user preferences when given id
#Input Parameters: user id
#Output: user preferences

def getUserPrefs(id):
    userPrefs = preferences.find_one({"user_id":id},{"_id":0,"prefs":1})
    return userPrefs

#Function to initialize the data set
#Input Parameters: Raw data set
#Output: Optimized data set

data = {}

def initializeDataSet():
    collection = db.preferences.find()
    for doc in collection:
        user_id = doc['user_id']
        prefs = doc['prefs']
        
        final = {}
        for item in prefs:
            final[item['place_id']] = item['rating']
        data[user_id] = final
    return data
    