import pandas as pd
from sklearn.linear_model import LinearRegression

#Function to return the normalized prediction for response
def getPredictionForNetwork(array):

    data = pd.read_csv('csv/TrainingSet/two_training.csv', sep=',', na_values="")

    # Train the model
    X = data[['gender', 'age_gap', 'wall_words', 'likes', 'locations_together', 'photos_together', 'user_friends', 'mutual_strength', 'last_comm']]
    y = data.response
    lm = LinearRegression(normalize=False)
    lm.fit(X, y)

    # Predict on the test data

    prediction = lm.predict(array)
    normalized = (prediction - 1.0)/(5.0-1.0)
    return (normalized)


#x = getPredictionForNetwork(np.array([1,2,2345,34,23,32,23,0.9,0]))
#print (x)

