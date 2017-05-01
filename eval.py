from pymongo import MongoClient
from crud import *
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
from pearson_similarity import *
from init import *

client = MongoClient('localhost', 27017)
db = client.script

#Initializing the test and training data sets for use
training_data,test_data = initializeDataSet()

#Getting the user average rating values
avgs = calAverages(training_data)

#Calcualting the user-user similiarities based on locations only
all_sims = calSimilarities(training_data,avgs)


#Function to get the existing locations for a given user
def get_existing_locs(user,data):
    user_prefs = data[user]
    locations = []
    for key in user_prefs.items():
        #Check if in preferences of other users
        if(not isNewLocation(key)):
            locations.append(key)
    print (locations)


#Function to return the mean absolute error
def get_mean_absolute_error(actual,predicted):
    return mean_absolute_error(actual,predicted)


#Function to extract the locations in the test set
def extract_test_locations_for_user(test_set,user):
    if(user in test_set):
        prefs = test_set[user]
        locations = []
        actual = []
        for key,value in prefs.items():
            locations.append(key)
            actual.append(value)

        return(locations,actual)


#Function to get the the ratings
def get_predicted_ratings(ratings,locations):
    predicted = []
    for loc in locations:
        predicted.append(ratings[loc])
    return predicted


#Function to calculate the errors for all users
def calculate_errors():
    actual_final = []
    predicted_final = []

    #Get all user ids
    users = db.preferences.distinct('user_id')
    for user in users:
        locations, actual = extract_test_locations_for_user(test_data,user)
        for i in actual:
            actual_final.append(i)
        #Rate the locations for existing user
        a,b = rateLocations(training_data,user,locations,avgs)
        predicted = get_predicted_ratings(a,locations)
        for i in predicted:
            predicted_final.append(i)

    mae = mean_absolute_error(actual_final,predicted_final)
    rms = sqrt(mean_squared_error(actual_final,predicted_final))

    print (mae)
    print (rms)
