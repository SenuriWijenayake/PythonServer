from dummyData import * 
from paper import *
from critics import *

a = []
loc = 'Loc6'
active = 'User1'
other = 'User3'
n = 4
# To calculate the similarity index between two users
#a = pearson_similarity (data,active,other)

#Get the top n users similar to a given user
#a = topSimilarUsers(data,active,4)

#Rating the locations based on the similar user preference
#a = rateLocations(data,active,loc)

a = data
print (a)