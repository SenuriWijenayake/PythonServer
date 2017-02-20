from pearson_similarity import *
from crud import *

a = []
b = []
active = "1"
other = "2"
location = "11"
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

#Lets look at the existing user - existing location scenario
#We get a set of candidate locations from the GIS
#For each location we need to provide a rating based on the ratings of similar users

#Get the top n users similar to the active user who have visited the particualr location
#a = topSimilarUsersForLocation(data,active,location,n,pearson_similarity)

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














