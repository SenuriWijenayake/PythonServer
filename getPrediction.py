import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#Function to return the prediction for response
def getPredictionForNetwork(array):

    data = pd.read_csv('csv/TrainingSet/two_training.csv', sep=',', na_values="")

    # Train the model
    X = data[['gender', 'age_gap', 'wall_words', 'likes', 'locations_together', 'photos_together', 'user_friends', 'mutual_strength', 'last_comm']]
    y = data.response
    lm = LinearRegression(normalize=False)
    lm.fit(X, y)

    # Predict on the test data

    prediction = lm.predict(array)
    return (prediction)



