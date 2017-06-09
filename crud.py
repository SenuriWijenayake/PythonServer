#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.script
preferences = db.preferences
users = db.users
locationPosts = db.locationPosts
friends = db.friends
locations = db.locations
feed = db.feeds

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
    new_count = 0
    new_users = {}
    for doc in collection:
        new_count += 1
        if(new_count<=40):

            user_id = doc['user_id']
            prefs = doc['prefs']
            num = len(prefs)
            count = 0
            benchmark = int(num/2)
            final_train = {}
            final_test = {}

            for item in prefs:
                count += 1
                if (count in range(0,benchmark+1)):
                    final_train[item['google_place_id']] = item['rating']
                if (count in range(benchmark+1,num+1)):
                    final_test[item['google_place_id']] = item['rating']

            training_data[user_id] = final_train
            test_data[user_id] = final_test

        if(new_count>40):
            user_id = doc['user_id']
            prefs = doc['prefs']
            my_prefs = {}
            for item in prefs:
                my_prefs[item['google_place_id']] = item['rating']

            new_users[user_id] = my_prefs

    return training_data,test_data,new_users
    
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
        min_age = age - 3
        max_age = age + 3
        
        if user_gender == gender and user_age in range(min_age,max_age+1):
            result[user] = 1
    
    return result

#Function to see if the location is a new location or not
def isNewLocation (location,active):
    cursor = preferences.find_one({'prefs': { '$elemMatch': {'google_place_id': 'ChIJLSrJAu-B4zoRQvotWplYx_c'}}, 'user_id' : {'$ne' : active}})
    if (cursor == None):
        return True
    else:
        return False

#Function to see if the location is a new location in the training data set
def isNewLocationTraining (data,location,active):
    result = True
    for user in data:
        if (user != active):
            for pref in data[user]:
                if (pref == location):
                    result = False
    return result

#Function to return the details of a location
def getLocationDetails (location):
    details = locations.find_one({"id":location})
    return details

#Function to get locations matching a set of tags, the region and visited bu a given set of users
def filterLocations (region,tags,ids):
    result = list(locations.find({ '$and' : [ {'id': {'$in' : ids }} , {'area': region }, {'types': { '$in' : tags }}]}))
    return result

#Function to get locations matching a set of tags, the region and visited bu a given set of users
def filterLocationsWithoutRegion (tags,ids):
    result = list(locations.find({ '$and' : [ {'id': {'$in' : ids }} , {'types': { '$in' : tags }}]}))
    return result

#Function to extract users with a given age range and gender other than the active user
def getUsersInAgeAndGender(active,age,gender):
    min_age = age - 3
    max_age = age + 3
    result = list(users.find({ 'id' : { '$ne' : active } ,'gender' : gender, 'age' : { '$gte' : min_age , '$lte' : max_age }}, {'_id' : 0, 'id' : 1}))
    return result

#Function to extract users with a given age range and gender other than the active user
def getUsersInAgeAndGenderTraining(active,age,gender):
    ids = []
    for key in training_data:
        ids.append(key)
    min_age = age - 3
    max_age = age + 3
    result = list(users.find({ 'id' : { '$in' : ids } ,'gender' : gender, 'age' : { '$gte' : min_age , '$lte' : max_age }}, {'_id' : 0, 'id' : 1}))
    return result



#Function to return the friend list of a given user
def getFriends(id):
    result = friends.find_one({"id":id},{"_id":0,"friends":1})
    return result

#Function to return ids of all the users
def getAllUsers():
    result = users.find({},{"_id":0,"id":1})
    return  result

#Function to extract a location profile
def get_location_id(location_name):
    profile = db.locations.find_one({'name':location_name},{'_id':0})
    return profile['id']


#Function to remove duplicates in locations
def remove_duplicates ():
    #Get all distinct ids
    distinct_ids = []
    distinct_ids = db.locations.distinct('id')
    print (len(distinct_ids))

    for tuple in distinct_ids:
        duplicates = []
        duplicates = db.locations.find({"id" : tuple}, {"_id" : 1})
        #Remove the first tuple id to be kept in the database
        remove_ids = []
        count = 0
        dups = list(duplicates)

        for tup in dups:
            if (count == 0):
                count += 1
            else:
                remove_ids.append(tup)

        length = len(remove_ids)
        if length is not 0:
            for id in remove_ids:
                db.locations.remove({"_id" : id['_id']})


#Function to create an array of user ids
def getAllUserIds():
    users = list(getAllUsers())
    all_users = []
    for user in users:
        all_users.append(user['id'])
    return all_users

#Function to get user feed
def getFeedOfUser(active):
    result = feed.find_one({'user_id':active},{'_id':0})
    return result
