from pearson_similarity import *
from crud import *
from init import *
from sklearn.metrics import mean_absolute_error
from math import sqrt

#Initializing the test and training data sets for use
training_data,test_data = initializeDataSet()

#Getting the user average rating values
avgs = calAverages(training_data)

#Calcualting the user-user similiarities based on locations only
all_sims = calSimilarities(training_data,avgs)

active = '1665852693730402'

#Always give this as an array
location = ['ChIJtTR_a0FF4joRDlYCqyEn03s','ChIJ1So3Yt5b4joRqtiBSKHxWig']
n = 2

a = topSimilarUsersForLocation(training_data,active,location,n,pearson_similarity,avgs)
b = rateLocations(training_data,active,location,avgs)

actual = [3,4]
predicted = [3.5643441891547227,4.268863122171946]

mae = mean_absolute_error(actual, predicted)
print (mae)

