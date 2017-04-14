from pearson_similarity import *
from crud import *
from init import *

#Initializing the test and training data sets for use
training_data,test_data = initializeDataSet()

#Getting the user average rating values
avgs = calAverages(training_data)

#Calcualting the user-user similiarities based on locations only
all_sims = calSimilarities(training_data,avgs)

