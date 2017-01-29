from pearson_similarity import *
from crud import userPrefs

a = []
active = "0"
other = "1"
n = 5
loc = ["Zoo6","Store1"]
location = "Zoo6"

# To calculate the similarity index between two users
#a = pearson_similarity (userPrefs,active,other)

#Get the top n users similar to a given user
#a = topSimilarUsers(userPrefs,active,n,pearson_similarity)

#Rating the locations based on the similar user preference
#a = rateLocations(userPrefs,active,loc)

#a = topSimilarUsersForLocation(userPrefs,active,location,n,pearson_similarity)
#b = getKValue(a)

a = rateLocations(userPrefs,active,loc)
print(a)



