from math import sqrt
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

def topSimilarUsers(data,subject,n):
    #Calculate r for subject and every other user
    similarity_scores = [(pearson_similarity(data,subject,other),other) for other in data if other!= subject]
    
    similarity_scores.sort()
    similarity_scores.reverse()
    
    return similarity_scores[0:n]

#Function to calculate k for a given location
#Input Paramters: active user, data set, location
#Output: k

def getKValue(data,active,loc):
    
    users = {}
    sumSim = 0
    
    #Get the users who have gone to the given location and their similarities
    for user in data:
        for item in data[user]:
            if item == loc:
                users.setdefault(user,'')
                users[user] = pearson_similarity(data,active,user)
                sumSim += users[user]
                
    n = len(users)
    k = sumSim/n
    
    return k,users
    
def getKey(item):
    return item[1]


#Function to rate a given set of locations

def rateLocations(data,active,locations):
    locations = ['Loc6','Loc3']
    total = 0
    rated_locations = {}
    ranked_locations = []
    
    for loc in locations:
        k, users = getKValue(data,active,loc)
        
        for user in users:
            rating = data[user][loc] 
            average = statistics.mean(data[user][i] for i in data[user])
            norm_rate = rating - average
            norm_sim_product = users[user] * norm_rate
            total += norm_sim_product
        
        #Average rating of the active user
        active_avg = statistics.mean(data[active][i] for i in data[active])
        rated_locations[loc] = (active_avg + k * total)
    
    ##Sorting the dictionary
    final_locations = sorted(rated_locations, key=rated_locations.get, reverse=True)

    return final_locations