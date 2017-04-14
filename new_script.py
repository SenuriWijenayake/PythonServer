from pearson_similarity import *
from crud import *
from init import *

#Initializing the data set for use
data = initializeDataSet()

#Getting the user average rating values
avgs = calAverages(data)

#Calcualting the user-user similiarities based on locations only
all_sims = calSimilarities(data,avgs)

