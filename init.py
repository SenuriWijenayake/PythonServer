#This is the initialization script
from math import sqrt
from crud import *
import statistics

#Fucntion to calculate the similarity between two users using the Pearsons correlation coefficient
##Parameters: Data set, id of person one, id of person two
##Output: corelation coefficient

def pearson_similarity (data,p1,p2,avgs):
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
    avgx = avgs[p1]
    avgy = avgs[p2]

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

#Function to calculate the user rating averages for all the users
#Access the average of the active user as avgs [active]
def calAverages(data):
    all_averages = {}
    for user in data:
        mean_rating = statistics.mean(data[user][i] for i in data[user])
        all_averages[user] = mean_rating
    return all_averages

#Function to calculate the Pearson Similarities for the users and store them in a matrix
#Access the cimilarity value between active user and other user as all_sims[active][other]
def calSimilarities(data,avgs):
    #Get the number of users in the system
    num_users = len(data)
    all_sims = {}
    for active in data:
        my_sims = {}
        for user in data:
            if user != active:
                sim = pearson_similarity(data,active,user,avgs)
                my_sims[user] = sim
        all_sims[active] = my_sims
    return all_sims

#Function to check if the profile is complete or not
def isProfileComplete(id):
    profile = dict(getUserDetails(id))
    length = profile.__len__()
    if length is 7:
        return True
    else:
        return False


#Function to return mutual friends for given two users
def findMutuals (active,other):
    mutuals = []
    #Get the friend lists of the two users
    userOne = getFriends(active)
    userTwo = getFriends(other)
    for friend in userOne['friends']:
        if friend in userTwo['friends']:
            mutuals.append(friend)
    return mutuals

#Function to filter mutuals over a attribute
def filterMutualFriends(active,other,attr):
    filtered_options = {}
    #Get mutual friends
    mutuals = findMutuals (active,other)
    #Filter using the attribute
    for friend in mutuals:
        total = len(mutuals)
        profile = dict(getUserDetails(friend))
        if(attr in profile) and (profile[attr] not in filtered_options):
            filtered_options[profile[attr]] = 1
        elif (attr in profile) and (profile[attr] in filtered_options):
            filtered_options[profile[attr]] += 1
    return filtered_options,total

#Function to calculate the profile similarity between two given users
#Input Parameters : the two ids of the users
#Output : the profile similarity
def calProfileSimilarity(u,x):
    #Check if the two profiles are complete
    active = dict(getUserDetails(u))
    other = dict(getUserDetails(x))
    if(isProfileComplete(u)) and (isProfileComplete(x)):
        count = 0
        if(active['age'] == other['age']):
            count += 1
        if(active['religion'] == other['religion']):
            count += 1
        if(active['hometown'] == other['hometown']):
            count += 1
        if(active['education'] == other['education']):
            count += 1
        if(active['gender'] == other['gender']):
            count += 1
        profSim = count/5
        return profSim

    #If the profiles are not complete
    else:
        #Take active user first and identify missing attributes
        attributes = ['age','hometown','gender','education','religion']
        for attr in attributes:
            if (attr not in active):
                #Find the available options, their frequency and total mutuals with given attribute
                filtered_options,total = filterMutualFriends(active['id'],other['id'],attr)
                print (filtered_options,total)




calProfileSimilarity("38","1")


