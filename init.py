import pandas as pd
from sklearn.linear_model import LinearRegression
from rateLocations import *
from similarities import *
import warnings
import time

warnings.simplefilter("ignore", category=DeprecationWarning)
start_time = time.time()

def plan_my_trip(user,locations):

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
    #print (all_sims)

    # user = "1665852693730402"
    # #user = "16658526937304023"
    # locations = [
    #     {
    #         "area" : " Peradeniya",
    #          "latitude" : 7.2565929,
    #          "name" : "University of Peradeniya",
    #          "id" : "ChIJ89kP1Lkv3YARr3RXkCQuMsY",
    #          "longitude" : 80.5966093,
    #          "rating" : 4.7,
    #          "types" : [
    #              "university",
    #             "point_of_interest",
    #             "establishment"
    #     ]},
    #     {
    #         "name" : "National Museum of Galle",
    #         "longitude" : 80.2170162,
    #         "latitude" : 6.0288631,
    #         "rating" : 4.2,
    #         "types" : [
    #             "museum",
    #             "point_of_interest",
    #             "establishment"
    #         ],
    #         "id" : "ChIJs_O3o0BZ4joRmOpvo3RHzms",
    #         "area" : " Galle"
    #     }
    # ]

    x = rateLocations(training_data,user,locations,avgs,all_sims)
    return (x)
    #print (x)
    #print("--- %s seconds ---" % (time.time() - start_time))
