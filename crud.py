#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
preferences = db.preferences
users = db.users

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
    
#Function to return the details of a user
def getUserDetails (id):
    user = users.find_one({"id":id},{"_id":0})
    return user

#Function to filter out the users with given age and gender
def filterUsersOnAgeGender (users,age,gender):
    result = {}
    for user in users:
        
        details = getUserDetails(user)
        user_age = details['age']
        user_gender = details['gender']
        min_age = age - 5
        max_age = age + 5
        
        if user_gender == gender and user_age in range(min_age,max_age+1):
            result[user] = 1
    
    return result
    
    
