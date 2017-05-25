#This is the initialization script
from math import sqrt,log10
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


#Fucntion to include the basic profile similarity function to the pearson correlation
##Parameters: Data set, id of person one, id of person two, avgs
##Output: modified correlation coefficient

def pearson_profile_similarity_basic (data,p1,p2,avgs,profile_sims):
    #Get the pearson correlation coefficient for the two users
    basic = pearson_similarity(data,p1,p2,avgs)
    #Get the profile similarity for the two users
    prof_sim = profile_sims[p1][p2]
    avg_profile_sim = statistics.mean(profile_sims[p1][i] for i in profile_sims[p1])
    r = basic * (prof_sim - avg_profile_sim)
    return r


#Function to calculate the user rating averages for all the users
#Access the average of the active user as avgs [active]
def calAverages(data):
    all_averages = {}
    for user in data:
        mean_rating = statistics.mean(data[user][i] for i in data[user])
        all_averages[user] = round(mean_rating,1)
    return all_averages

#Function to calculate the Pearson Similarities for the users and store them in a matrix
#Access the cimilarity value between active user and other user as all_sims[active][other]
def calSimilarities(data,avgs,similarity):
    #Get the number of users in the system
    num_users = len(data)
    all_sims = {}
    profile_sims = calProfileSimilarities()
    for active in data:
        my_sims = {}
        for user in data:
            if user != active:
                if(similarity == pearson_similarity):
                    sim = similarity(data,active,user,avgs)
                    my_sims[user] = sim
                if (similarity == pearson_profile_similarity_basic):
                    sim = similarity(data,active,user,avgs,profile_sims)
                    my_sims[user] = sim
        all_sims[active] = my_sims
    return all_sims

#Function to check if the profile is complete or not
def isProfileComplete(id):
    profile = dict(getUserDetails(id))
    length = profile.__len__()
    if length is 8:
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
    mut_count = len(mutuals)
    #Check if there are mutuals
    if (mut_count != 0):
        #Filter using the attribute
        for friend in mutuals:
            count = 0
            profile = dict(getUserDetails(friend))
            if(attr in profile) and (profile[attr] not in filtered_options):
                filtered_options[profile[attr]] = 1
                count += 1
            elif (attr in profile) and (profile[attr] in filtered_options):
                filtered_options[profile[attr]] += 1
                count += 1
        #Check if there are filtered mutuals
        if (count != 0):
            return filtered_options,count
        return (0,0)
    return (0,0)

#Function to filter friends over a attribute
def filterFriends(id,attr):
    filtered_options = {}
    #Get the friend list
    friendList = getFriends(id)

    #There are friends
    if(len(friendList) != 0):
        for friend in friendList['friends']:
            count = 0
            profile = dict(getUserDetails(friend))
            if(attr in profile) and (profile[attr] not in filtered_options):
                filtered_options[profile[attr]] = 1
                count += 1
            elif (attr in profile) and (profile[attr] in filtered_options):
                filtered_options[profile[attr]] += 1
                count += 1
        if(count != 0):
            return filtered_options,count
        return (0,0)
    return (0,0)


#Function to calculate the profile similarity between two given users
#Input Parameters : the two ids of the users
#Output : the profile similarity
def calProfileSimilarity(u,x):
    #Check if the two profiles are complete
    active = dict(getUserDetails(u))
    other = dict(getUserDetails(x))

    #Define the attributes to be predicted and attributes used for sim measurement
    attributes = ['age','hometown','gender','education','religion']
    attr_for_sims = ['age','hometown','gender','education','religion']

    if(isProfileComplete(u)) and (isProfileComplete(x)):
        count = 0
        for attr in attributes:
            if(active[attr] == other[attr]):
                count += 1
        profSim = count/5
        return profSim

    #If the profiles are not complete
    else:
        #Create a copy of active and other users
        other_copy = other.copy()
        act_copy = active.copy()

        for attr in attributes:
            #Complete the profile of user one
            if (attr not in active):
                #Find the available options, their frequency and total mutuals with given attribute
                #If there are mutual friends
                filtered_options,total = filterMutualFriends(active['id'],other['id'],attr)
                if total != 0:
                    #Sort the dict and get the most frequent entry
                    options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                    predicted_value = options[0][0]
                    probability = options[0][1]/total
                    act_copy[attr] = predicted_value
                else:
                    #There are no mutual friends with the attribute or no mutuals
                    #Use friends to filter the frequent observations
                    filtered_options,total = filterFriends(active['id'],attr)
                    if total != 0:
                        #Sort the dict and get the most frequent entry
                        options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                        predicted_value = options[0][0]
                        probability = options[0][1]/total
                        act_copy[attr] = predicted_value
                    else:
                        #Drop the attribute from the list
                        if (attr in attr_for_sims):
                            attr_for_sims.remove(attr)

            #Complete the profile of user two
            if (attr not in other):
                #Find the available options, their frequency and total mutuals with given attribute
                filtered_options,total = filterMutualFriends(other['id'],active['id'],attr)
                if total != 0:
                    #Sort the dict and get the most frequent entry
                    options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                    predicted_value = options[0][0]
                    probability = options[0][1]/total
                    other_copy[attr] = predicted_value
                else:
                    #There are no mutual friends with the attribute or no mutuals
                    #Use friends to filter the frequent observations
                    filtered_options,total = filterFriends(other['id'],attr)
                    if total != 0:
                        #Sort the dict and get the most frequent entry
                        options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                        predicted_value = options[0][0]
                        probability = options[0][1]/total
                        other_copy[attr] = predicted_value
                    else:
                        #Drop the attribute from the list
                        if (attr in attr_for_sims):
                            attr_for_sims.remove(attr)

        #Once the profiles are temporarily completed, calculate the similarity
        count = 0
        for item in attr_for_sims:
            if(act_copy[item] == other_copy[item]):
                count += 1
        #Even if there are not many predicted attributes we still divide it by 5
        #If the values can't be predicted the users are not similar
        profSim = count/5
        return profSim

#Function to calcualte the profile similarities of users and store them
def calProfileSimilarities():
    #Get the ids of all the users
    all_users = list(getAllUsers())
    all_sims = {}
    for active in all_users:
        my_sims = {}
        for other in all_users:
            if (active['id'] is not other['id']):
                sim = calProfileSimilarity(active['id'],other['id'])
                my_sims[other['id']] = sim
        all_sims[active['id']] = my_sims
    return all_sims

#Function to see if two users are friends or not
def isFriends(u,x):
    u_list = getFriends(u)
    if (len(u_list['friends']) is not 0) and x in u_list['friends']:
        return True
    return False

#Function to calculate the number of edges in the friendship graph
def getEdgesFriendGraph(u):
    #Get all the friends of the active user
    count = 0
    result = getFriends(u)
    friends = result['friends']
    list = friends.copy()
    num_friends = len(friends)
    #Get the direct connections
    count += num_friends

    #Get the connections between friends in the friend graph
    for friend in friends:
        result = getFriends(friend)
        friendList = result['friends']
        for user in list:
            if (user in friendList):
                count += 1
        list.remove(friend)
    return count

#Function to calcualte the number of edges in the mutual friends graph
def getEdgesMutualFriendGraph(active,other):
    mutuals = findMutuals (active,other)
    #Both users are connected to the mutual friends
    count = len(mutuals) * 2
    list = mutuals.copy()
    #Get the inter-friend links
    for friend in mutuals:
        result = getFriends(friend)
        friendList = result['friends']
        for user in list:
            if (user in friendList):
                count += 1
        list.remove(friend)
    return count


#Function to calculate the network similarities between two strangers using mutual friends
def mutualBasedNetworkSimilarity(active,other):
    #Check if the two users are not friends but has mutual friends
    mutuals = findMutuals (active,other)
    if(isFriends(active,other) is not True) and (len(mutuals) is not 0):
        edges_friends = getEdgesFriendGraph(active)
        edges_mutual_friends = getEdgesMutualFriendGraph(active,other)
        sim = log10(edges_mutual_friends)/log10(2*edges_friends)
        return sim
    #If the two users are not friends and have no mutuals
    if (isFriends(active,other) is not True) and (len(mutuals) is 0):
        return 0

    #If two users are friends calculate the tie strength between the two users


#Function to return a completed profile prediction for a user
def getProfilePrediction(active,other):

    #Define the attributes to be predicted and attributes used for sim measurement
    attributes = ['age','hometown','gender','education','religion']
    attr_for_sims = ['age','hometown','gender','education','religion']

    other_copy = other.copy()

    for attr in attributes:
        #Complete the profile of user two
        if (attr not in other):
            #Find the available options, their frequency and total mutuals with given attribute
            filtered_options,total = filterMutualFriends(other['id'],active['id'],attr)
            if total != 0:
                #Sort the dict and get the most frequent entry
                options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                predicted_value = options[0][0]
                other_copy[attr] = predicted_value
            else:
                #There are no mutual friends with the attribute or no mutuals
                #Use friends to filter the frequent observations
                filtered_options,total = filterFriends(other['id'],attr)
                if total != 0:
                    #Sort the dict and get the most frequent entry
                    options = sorted(filtered_options.items(), key = lambda x : x[1], reverse=True)
                    predicted_value = options[0][0]
                    other_copy[attr] = predicted_value
    return other_copy
