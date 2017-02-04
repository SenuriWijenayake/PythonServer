from pearson_similarity import *
from crud import *

a = []
active = "1"
other = "10"
n = 5
loc = ["11","1"]
location = "1"

#Initialize data set
data = initializeDataSet()

#To calculate the similarity index between two users
#a = pearson_similarity (data,active,other)

#Get the top n users similar to a given user
#a = topSimilarUsers(data,active,n,pearson_similarity)

#Rating the locations based on the similar user preference
a = rateLocations(data,active,loc)

#a = topSimilarUsersForLocation(data,active,location,n,pearson_similarity)

print(a)




