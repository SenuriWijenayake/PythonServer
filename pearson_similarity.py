from math import sqrt
from crud import *
import statistics
import operator

#Fucntion to calculate the similarity between two users using the Pearsons correlation coefficient
##Parameters: Data set, id of person one, id of person two
##Output: corelation coefficient

def pearson_similarity (data,p1,p2):
    #Get the list of similar locations between the users
    similar_items = {}
    for item in data[p1]:
        if item in data[p2]:
            similar_items[item] = 1
            
    if len(similar_items) == 0:
        return 0
    
    #Get the variables ready for the calculation
    n = len(similar_items)
    
    #Get the average for each user
    avgx = statistics.mean(data[p1][i] for i in data[p1])
    avgy = statistics.mean(data[p2][i] for i in data[p2])
        
    #Calculate the sum of normalized squared preferences
    sumx2 = sum(pow(data[p1][item] - avgx,2) for item in similar_items)
    sumy2 = sum(pow(data[p2][item] - avgy,2) for item in similar_items)
    
    #sum of products
    sumxy = sum((data[p1][item] - avgx) * (data[p2][item] - avgy) for item in similar_items)
    
    #Pearson calculation for r
    num = sumxy
    den = sqrt(sumx2 * sumy2)
    
    if den == 0:
        return 0
    r = num/den

    return r

#Funtion to return top n similar users
#Input Parameters : data set, key person, number of similar users (n)
#Output : r between the two users, other user

def topSimilarUsers(data,subject,n,similarity):
    #Calculate r for subject and every other user
    similarity_scores = [(similarity(data,subject,other),other) for other in data if other!= subject]
    
    similarity_scores.sort()
    similarity_scores.reverse()
    
    return similarity_scores[0:n]

#Funtion to return top n similar users who have gone to a given location
#Input Parameters : data set, key person, location, number of users, similarity measure
#Output : top n similar users, and the similarity

def topSimilarUsersForLocation(data,subject,location,n,similarity):
    
    similarity_scores = {}
    sorted_users = {}

    #Get the users who have been to a particular location
    for user in data:
        if user != subject:
            for i in data[user]:
                if location == i:
                    #Calculate r for subject and the user
                    r = similarity(data,subject,user)   
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

def rateLocations(data,active,locations):

    rated_locations = {}
    
    n = 5
    similarity = pearson_similarity

    #Check if the locations list is null
    if locations == []:
        return "No locations meeting criteria"

    #Check if the user is a new user or not
    user_status = isNewUser(active)
    if (user_status):
        #Handling new user scenario - user has no ratings
        for loc in locations:
            #Get users in similar age and gender who have been to the given location
            users = topUsersOnAttributesForLocation (data,active,loc)
            print(users)
            #Get the average ratings of the users for location
            total = sum(data[user][loc] for user in users)
            rating = total/len(users)
            
            rated_locations[loc] = rating
        
        print(rated_locations,total,rating,len(users))

        ##Sorting the dictionary
        final_locations = sorted(rated_locations, key=rated_locations.get, reverse=True)

    return final_locations
                
    #Not a new user   
    if (not user_status):    
        #Get the average rating of active user
        active_avg = statistics.mean(data[active][i] for i in data[active])
        
        for loc in locations:

            total = 0
            #Get the top similar users for the locations
            users = topSimilarUsersForLocation(data,active,loc,similarity)

            #Get the k value for the location
            k = getKValue(users)

            for user in users:
                #Get the user rating for the location
                id = user[0]
                rating = data[id][loc]

                #Get the average rating of the user
                average = statistics.mean(data[id][i] for i in data[id])
                norm_rate = rating - average
                norm_sim_product = user[1] * norm_rate
                total += norm_sim_product

            #Calculate the score of the location
            rated_locations[loc] = (active_avg + k * total)

        print(rated_locations)

        ##Sorting the dictionary
        final_locations = sorted(rated_locations, key=rated_locations.get, reverse=True)

        return final_locations

#Function to determine whether the user has existing preferences or not
def isNewUser(active):
    result = getUserPrefs("25")
    if (result == None):
        return True
    else:
        return False
    
#Function to get the top users based on age and gender for a given location
def topUsersOnAttributesForLocation (data,subject,location):

    #Get the users who have been to a particular location
    res = getUsersForLocation (data,subject,location)
    
    #Get the age and gender of the active user
    details = getUserDetails (subject)
    user_age = details['age']
    user_gender = details['gender']
    
    #Filter users who are in the same age range and gender
    users = filterUsersOnAgeGender(res,user_age,user_gender)
    return users

#Function to get the users who have been to a particular location other than the active user
def getUsersForLocation (data,subject,location):
    users = {}
    for user in data:
        if user != subject:
            for i in data[user]:
                if location == i:
                    users[user] = 1
    return users