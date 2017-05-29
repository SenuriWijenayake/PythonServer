from pymongo import MongoClient
from crud import *
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
from rateLocations import *
from similarities import *

client = MongoClient('localhost', 27017)
db = client.script

#Define the similarity measurement
similarity = pearson_profile_network_similarity

#Initializing the test and training data sets for use
training_data,test_data,new_users = initializeDataSet()

#Getting the user average rating values
avgs = calAverages(training_data)

#Calcualting the user-user similiarities based on locations only
all_sims = calSimilarities(training_data,avgs,similarity)



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

    #Get all existing ids
    users = test_data.keys()
    for user in users:
        locations, actual = extract_test_locations_for_user(test_data,user)
        for i in actual:
            actual_final.append(i)
        #Rate the locations for existing user
        a,b = rateLocations(training_data,user,locations,avgs,all_sims)
        predicted = get_predicted_ratings(a,locations)
        for i in predicted:
            predicted_final.append(i)

    my_new_users = new_users.keys()
    for user in my_new_users:
        locations, actual = extract_test_locations_for_user(new_users,user)
        for i in actual:
            actual_final.append(i)
        #Rate the locations for new user
        a,b = rateLocations(training_data,user,locations,avgs,all_sims)
        predicted = get_predicted_ratings(a,locations)
        for i in predicted:
            predicted_final.append(i)


    mae = mean_absolute_error(actual_final,predicted_final)
    rms = sqrt(mean_squared_error(actual_final,predicted_final))

    print (mae)
    print (rms)


#Function to calculate the accuracy of profile attribute predictions
def calculate_profile_prediction_accuracy():
    attributes = ['age','hometown','gender','education','religion']

    correct = {'age':0,'hometown':0,'gender':0,'education':0,'religion':0}
    totals = {'age':0,'hometown':0,'gender':0,'education':0,'religion':0}

    users = list(getAllUsers())
    for user in users:
        active = dict(getUserDetails(user['id']))
        for other in users:
            if (user['id'] is not other['id']):
                #Get the predicted profile
                other_prof = dict(getUserDetails(other['id']))
                other_copy = {'id':other_prof['id']}

                predicted_profile = getProfilePrediction(active,other_copy)

                for attr in attributes:
                    actual = other_prof[attr]
                    predicted = predicted_profile[attr]

                    totals[attr] = totals[attr] + 1

                    if (actual == predicted):
                        correct[attr] = correct[attr] + 1

    print ("Accuracy of age : " + str(correct['age']/totals['age']))
    print ("Accuracy of hometown : " + str(correct['hometown']/totals['hometown']))
    print ("Accuracy of religion : " + str(correct['religion']/totals['religion']))
    print ("Accuracy of education : " + str(correct['education']/totals['education']))
    print ("Accuracy of gender : " + str(correct['gender']/totals['gender']))

