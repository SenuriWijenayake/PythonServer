from pearson_similarity import *
from crud import *

a = []
b = []
active = "35"
other = "10"
n = 5
loc = ["11","1","15"]
location = "51"
users = ["1","2"]
tags = ["food","cafe"]

#Initialize data set
data = initializeDataSet()

#To calculate the similarity index between two users
#a = pearson_similarity (data,active,other)

#Get the top n users similar to a given user
#a = topSimilarUsers(data,active,n,pearson_similarity)

#Rating the locations based on the similar user preference
#a = rateLocations(data,active,loc)

#a = topSimilarUsersForLocation(data,active,location,n,pearson_similarity)

#a = rateLocations(data,"35",loc)
#b = rateLocations(data,"36",loc)

a = getNewLocationRating (location)
print(a)





