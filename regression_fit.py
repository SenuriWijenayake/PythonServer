import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split

data = pd.read_csv('csv/Raw/two.csv', sep=',', na_values="")
train_data, test_data = train_test_split(data,train_size=0.75)

# Train the model
X = train_data[['gender','age_gap', 'mutual_strength', 'wall_words', 'locations_together', 'user_friends', 'photos_together', 'likes', 'last_comm']]
y = train_data.response
lm = LinearRegression(normalize=False)
lm.fit(X, y)

# Predict on the test data
X_test = test_data[['gender', 'age_gap', 'mutual_strength', 'wall_words', 'locations_together', 'user_friends', 'photos_together', 'likes', 'last_comm']]
y_test = test_data.response
y_pred = lm.predict(X_test)

# Compute the root-mean-square
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(mae,rmse)
