#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.script
preferences = db.preferences
users = db.users
locations = db.locationPosts
friends = db.friends

#Function to retreieve user preferences when given id
#Input Parameters: user id
#Output: user preferences

def getUserPrefs(id):
    userPrefs = preferences.find_one({"user_id":id},{"_id":0,"prefs":1})
    return userPrefs

#Function to initialize the data set
#Input Parameters: Raw data set
#Output: Optimized data set

training_data = {}
test_data = {}

def initializeDataSet():
    collection = db.preferences.find()
    num = collection.count()
    benchmark = int(num/2)
    count = 0
    
    for doc in collection:
        count += 1
        user_id = doc['user_id']
        prefs = doc['prefs']
        final = {}
        for item in prefs:
            final[item['place_id']] = item['rating']

        if (count in range(0,benchmark+1)):
            training_data[user_id] = final
        if (count in range(benchmark+1,num+1)):
            test_data[user_id] = final
    return training_data,test_data
    
#Function to return the details of a user
def getUserDetails (id):
    user = users.find_one({"id":id},{"_id":0})
    return user

#Function to filter out a given set of users with given age and gender
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

#Function to see if the location is a new location or not
def isNewLocation (location):
    cursor = preferences.find_one({'prefs': { '$elemMatch': {'place_id': location}}})
    if (cursor == None):
        return True
    else:
        return False

#Function to return the details of a location
def getLocationDetails (location):
    details = locations.find_one({"id":location})
    return details

#Function to get locations matching a set of tags, the region and visited bu a given set of users
def filterLocations (region,tags,ids):
    result = list(locations.find({'id': {'$in' : ids }, 'area': region , 'types': { '$in' : tags }}))
    return result

#Function to extract users with a given age range and gender other than the active user
def getUsersInAgeAndGender(active,age,gender):
    min_age = age - 5
    max_age = age + 5
    result = list(users.find({ 'id' : { '$ne' : active } ,'gender' : gender, 'age' : { '$gte' : min_age , '$lte' : max_age }}, {'_id' : 0, 'id' : 1}))
    return result

#Function to return the friend list of a given user
def getFriends(id):
    result = friends.find_one({"id":id},{"_id":0,"friends":1})
    return result

#Function to return ids of all the users
def getAllUsers():
    result = users.find({},{"_id":0,"id":1})
    return  result

