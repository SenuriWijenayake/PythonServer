from pearson_similarity import *
from crud import *

a = []
b = []
other = "10"
n = 5

exist_user = "20"
exist_loc = ["11","1","15"]

new_user = "35"
new_loc = ["51","52"]

mix_location = ["11","1","15","51","52"]

#Initialize data set
data = initializeDataSet()

#To calculate the similarity index between two users
#a = pearson_similarity (data,active,other)

#Get the top n users similar to a given user
#a = topSimilarUsers(data,active,n,pearson_similarity)

#Rating the locations based on the similar user preference
#Existing user - Existing Locations
#a = rateLocations(data,exist_user,exist_loc)

#Existing User - New Locations
#a = rateLocations(data,exist_user,new_loc)

#New User - Existing Locations
#a = rateLocations(data,new_user,exist_loc)

#New User - New Locations
#a = rateLocations(data,new_user,new_loc)

#A mix of locations for a new user
#a = rateLocations(data,new_user,mix_location)

#A mix of locations for an existing user
a = rateLocations(data,exist_user,mix_location)

print(a)





