from pearson_similarity import *
from crud import userPrefs

a = []
active = "0"
other = "1"
n = 4
loc = ["Zoo6","Zoo7"]

# To calculate the similarity index between two users
#a = pearson_similarity (userPrefs,active,other)

#Get the top n users similar to a given user
a = topSimilarUsers(userPrefs,active,n,pearson_similarity)

#Rating the locations based on the similar user preference
a = rateLocations(userPrefs,active,loc)

print(a)



