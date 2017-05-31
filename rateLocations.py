from similarities import *
from collections import OrderedDict
import statistics
import operator
import itertools

#Funtion to return top n similar users who have gone to a given location
#Input Parameters : data set, key person, location, number of users, similarity measure
#Output : top n similar users, and the similarity

def topSimilarUsersForLocation(data,subject,location,n,all_sims,avgs):

    similarity_scores = {}
    sorted_users = {}

    #Get the users who have been to a particular location
    for user in data:
        if user != subject:
            for i in data[user]:
                if location == i:
                    #Calculate r for subject and the user
                    r = all_sims[subject][user]
                    similarity_scores[user] = r

    num = len(similarity_scores)

    #If new location (no users have gone to this place)
    if num == 0:
        return "New Location"

    #Sorting the object
    sorted_users = sorted(similarity_scores.items(), key=operator.itemgetter(1), reverse=True)

    num_users = len(sorted_users)

    #Only num_users number of users available
    if num_users < n:
        return sorted_users[0:num_users]

    return sorted_users[0:n]

#Function to calculate k for a given location
#Input Paramters: top n similar users and their similarity measures
#Output: k

def getKValue(users):

    sumSim = 0

    for user in users:
        sumSim += user[1]

    n = len(users)
    k = sumSim/n

    return k

#Function to rate a given set of locations
#Input Parameters: Set of locations, id of the active user, set of locations to be rated
#Output: Ranked locations

def rateLocations(data,active,locations,avgs,all_sims):

    rated_locations = {}

    n = 5

    #Check if the locations list is null
    if len(locations) == 0:
        return "No locations meeting criteria"

    #Check if the user is a new user or not
    user_status = isNewUser(active)
    if (user_status):
        print("User is a new user")
        #Handling new user scenario - user has no ratings
        for location in locations:
            loc = location['id']
            #Check if the location is a new location
            if(isNewLocationTraining(data,loc,active)):
                print("New Location - New user")
                #Handle new location
                rating = getNewLocationRatingForNewUser(location,active)
                rated_locations[loc] = round(rating,1)

            else:
                print("Existing Location - New user")
                #Get users in similar age and gender who have been to the given location
                users = topUsersOnAttributesForLocation (data,active,loc)

                total = 0
                tot_avg = 0
                #For each user get the location rating, average rating of user
                for user in users:

                    avg_user = avgs[user]
                    loc_rating = data[user][loc]
                    normalized_rating = loc_rating - avg_user
                    #Get the sum of the normalized ratings
                    total += normalized_rating
                    #Get the sum of averages
                    tot_avg += avg_user

                #Get the average of normalized ratings of the users for location
                den = len(users)
                if(den is 0):
                    print("Alert!")
                avg_of_avgs = tot_avg/den
                avg_norm_rating = total/den

                rating = avg_of_avgs + avg_norm_rating
                rated_locations[loc] = round(rating,1)

        print(rated_locations)
        ##Sorting the dictionary
        final_locations = sorted(rated_locations, key=rated_locations.get, reverse=True)
        return rated_locations, final_locations

    #Not a new user
    if (not user_status):
        print("Not a new user")
        #Get the average rating of active user
        active_avg = avgs[active]

        for location in locations:
            loc = location['id']
            #Check if the location is a new location
            if(isNewLocationTraining(training_data,loc,active)):
                print("New Location - Existing user")
                #Handle new location
                rating = getNewLocationRatingForExistingUser(location,active)
                rated_locations[loc] = round(rating,1)

            else:
                print("Existing Location - Existing user")
                total = 0
                #Get the top similar users for the locations
                users = topSimilarUsersForLocation(data,active,loc,n,all_sims,avgs)

                #Get the k value for the location
                k = getKValue(users)

                for user in users:
                    #Get the user rating for the location
                    id = user[0]
                    rating = data[id][loc]

                    #Get the average rating of the user
                    average = avgs[id]
                    norm_rate = rating - average
                    norm_sim_product = user[1] * norm_rate
                    total += norm_sim_product

                #Calculate the score of the location
                rated_locations[loc] = round((active_avg + k * total),1)

        print(rated_locations)

        ##Sorting the dictionary
        final_locations = sorted(rated_locations, key=rated_locations.get, reverse=True)

        return rated_locations, final_locations

#Function to determine whether the user has existing preferences or not
def isNewUser(active):
#    result = getUserPrefs(active)
#   if (result == None):
#       return True
#    else:
#        return False
    if(active in test_data.keys()):
        return False
    else:
        return True



#Function to get the top users based on age and gender for a given location
def topUsersOnAttributesForLocation (data,subject,location):

    #Get the users who have been to a particular location
    res = getUsersForLocation (data,subject,location)
    if (len(res) == 0):
        print ("No users")
    #Get the age and gender of the active user
    details = getUserDetails (subject)
    user_age = details['age']
    user_gender = details['gender']

    #Filter users who are in the same age range and gender
    users = filterUsersOnAgeGender(res,user_age,user_gender)
    if (len(users)is 0):
        users = res
    return users


#Function to get the users who have been to a particular location other than the active user
#Input Parameters: data set, active user, location
#Output: users who have been to the given location
def getUsersForLocation (data,subject,location):
    users = {}
    for user in data:
        if user != subject:
            for i in data[user]:
                if location == i:
                    users[user] = 1
    return users

#Function to handle new location for existing user
#Input Parameter: new location's id, user id
#Output: rating calculated for the new location

def getNewLocationRatingForExistingUser(loc,user):

    weights = {}
    top_locations = {}

    #Get location details
    details = loc
    area = details['area']
    tags = details['types']

    #Get the locations that the user has been to
    visited_ids = []
    for pref in training_data[user]:
        visited_ids.append(pref)

    #Out of the visited locations filter locations in same region having atleast one similar tag
    filtered_locations = filterLocations (area,tags,visited_ids)

    if (len(filtered_locations) == 0):
        filtered_locations = filterLocationsWithoutRegion (tags,visited_ids)

    if(len(filtered_locations) == 0):
        return 0

    #Calculate the tag similarity for each location
    for loc in filtered_locations:
        count = 0
        for tag in loc['types']:
            if tag in tags:
                count += 1
        if (count >= 1):
            #calculate the tag similarity
            den = len(tags) + len(loc['types'])
            sim = count/den
            weights[loc['id']] = sim

    top_locations = OrderedDict(sorted(weights.items(), key = lambda x : x[1], reverse=True))

    length = len(top_locations)
    if (length >= 5):
        locs = itertools.islice(top_locations.items(), 0, 5)
        den = 5
    else:
        locs = top_locations
        den = len(locs)
    print(locs)
    #Calcualte the average rating of the user
    average = statistics.mean(training_data[user][i] for i in training_data[user])

    #Calculate the sum of normalized and weighted ratings for each location
    total = 0
    for item in locs:
        #Get tag similarity
        if (isinstance(item,str)):
            id = item
        else:
            id = item[0]
        tag_sim = weights[id]

        #Get the user rating for given location
        user_rating = training_data[user][id]

        #Calculate the normalized weighted total rating
        total += (user_rating - average) * tag_sim

    #Calculate the average normalized rating
    #den = len(locs)
    avg_norm = total/den

    final_rating = average + avg_norm

    return final_rating


#Function to handle new location for new user
#Input Parameter: new location's id, user id
#Output: rating calculated for the new location
def getNewLocationRatingForNewUser(loc,active):

    weights = {}
    top_locations = {}

    #Get location details
    details_loc = loc
    area = details_loc['area']
    tags = details_loc['types']

    #Get the age and gender of the active user
    details = getUserDetails (active)
    user_age = details['age']
    user_gender = details['gender']

    #Find users who are similar in age and gender
    res = getUsersInAgeAndGenderTraining(active,user_age,user_gender)

    #Find all the locations visited by the given users
    visited_ids = []
    for user in res:
        user_id = user['id']

        #Get the locations that the user has been to
        for pref in training_data[user_id]:
            if pref not in visited_ids:
                visited_ids.append(pref)

    #Out of the visited locations filter locations in same region having atleast one similar tag
    filtered_locations = filterLocations (area,tags,visited_ids)

    if (len(filtered_locations) == 0):
        filtered_locations = filterLocationsWithoutRegion (tags,visited_ids)

    if(len(filtered_locations) == 0):
        return 0

    #Calculate the tag similarity for each location
    for loc in filtered_locations:
        count = 0
        for tag in loc['types']:
            if tag in tags:
                count += 1
        if (count >= 1):
            #calculate the tag similarity
            den = len(tags) + len(loc['types'])
            sim = count/den
            weights[loc['id']] = sim

    top_locations = sorted(weights.items(), key = lambda x : x[1], reverse=True)

    length = len(top_locations)
    if (length >= 5):
        locs = list(itertools.islice(top_locations, 0, 5))
    else:
        locs = list(top_locations)

    #Get location ids
    loc_ids = []
    for l in locs:
        loc_ids.append(l[0])

    #For each similar location find top similar users to active users who have visited that location
    rated_locations = {}
    location_outputs = []

    for location in loc_ids:

        total = 0
        tot_avg_two = 0
        group_total = 0
        similar_users = []
        loc_id = location

        for user in res:
            user_id = user['id']
            #If user has been to this location

            if (hasBeenToLocation(user_id, loc_id)):
                similar_users.append(user_id)

        #Considering the list of users who have been to the location
        #For each user get the location rating, average rating of user
        for user in similar_users:
            avg_user = statistics.mean(training_data[user][i] for i in training_data[user])
            loc_rating = training_data[user][loc_id]
            normalized_rating = loc_rating - avg_user

            #Get the sum of the normalized ratings
            total += normalized_rating
            #Get the sum of averages
            tot_avg_two += avg_user

        #Get the average of normalized ratings of the users for location
        den = len(similar_users)
        avg_of_avgs = tot_avg_two/den
        avg_norm_rating = total/den

        #Calcualte initial rating
        rating = avg_of_avgs + avg_norm_rating

        #Save location details

        top = dict(top_locations)
        sim_score = top[loc_id]
        location_outputs.append({'loc_id' : loc_id, 'rating' : rating, 'simScore' : sim_score})


    #Calculating the rating for new location
    tot = 0

    for l in location_outputs:
        tot += l['rating'] * l['simScore']

    den = len(location_outputs)

    final_rating = 3 + (tot/den)

    return final_rating

def hasBeenToLocation (user,loc):
    for item in training_data[user]:
        if item == loc:
            return True
    return False







