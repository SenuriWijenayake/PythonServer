import pandas as pd
from sklearn.linear_model import LinearRegression
from similarities import *
import warnings
import time

warnings.simplefilter("ignore", category=DeprecationWarning)
start_time = time.time()


#Define the similarity measurement
similarity = pearson_network_similarity_basic

#Initializing the test and training data sets for use
#Training set includes only 40 users and half of their preferences
training_data,test_data,new_users = initializeDataSet()

#Getting the user average rating values
print ("Calculating user average ratings")
avgs = calAverages(training_data)

#Initializing the regression model
print ("Initilizing the regression model")
data = pd.read_csv('csv/TrainingSet/final_training_set.csv', sep=',', na_values="")

# Train the model
X = data[['gender','locations_together', 'mutual_strength', 'likes']]
y = data.response
lm = LinearRegression(normalize=False)
lm.fit(X, y)

#Calcualting the user-user similiarities based on the defined similarity measure
print ("Calculating all user similarities")
all_sims = calSimilarities(training_data,avgs,similarity,lm)

print ("Initialization completed")
