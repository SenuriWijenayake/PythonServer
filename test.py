from math import sqrt

#Fucntion to calculate the similarity between two users using the Pearsons correlation coefficient
##Parameters: Data set, id of person one, id of person two
##Output: corelation coefficient

def pearson_similarity (data,p1,p2):
    #Get the list of similar items between the users
    similar_items = {}
    for item in data[p1]:
        if item in data[p2]:
            similar_items[item] = 1
            
    if len(similar_items) == 0:
        return 0
    
    #Get the variables ready for the calculation
    n = len(similar_items)

    #Calculate the sum of individual preferences
    sumx = sum(data[p1][item] for item in similar_items)
    sumy = sum(data[p2][item] for item in similar_items)
    
    #Calculate the sum of squared preferences
    sumx2 = sum(pow(data[p1][item],2) for item in similar_items)
    sumy2 = sum(pow(data[p2][item],2) for item in similar_items)
    
    #sum of products
    sumxy = sum(data[p1][item] * data[p2][item] for item in similar_items)
    
    #Pearson calculation for r
    num = n * sumxy - (sumx * sumy)
    den = sqrt((n * sumx2 - pow(sumx,2))*(n * sumy2 - pow(sumy,2)))
    
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

#Function to get recommendations for a person by using a weighted average of every other user's rankings
#Input Parameters: data set, subject, number of recommendations
#Output: ranked locations

def getRecommendations(prefs,person,n,similarity=pearson_similarity):
	totals = {}
	simSums = {}

	for other in prefs:
		#don't compare me to myself
		if other == person:
			continue
		sim = similarity(prefs,person,other)

		#ignore scores of zero or lower
		if sim <= 0: 
			continue
		for item in prefs[other]:
			#only score books i haven't seen yet
			if item not in prefs[person] or prefs[person][item] == 0:
				#Similarity * score
				totals.setdefault(item,0)
				totals[item] += prefs[other][item] * sim
				#Sum of similarities
				simSums.setdefault(item,0)
				simSums[item] += sim

	#Create the normalized list
	rankings = [(total/simSums[item],item) for item,total in totals.items()]

	#Return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings[0:n]
