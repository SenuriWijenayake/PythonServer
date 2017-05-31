import pandas
from statsmodels.formula.api import ols
import patsy
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np

#vif_file = open('vif.txt','w')
summary = open ('summary.txt', 'w')
df = pandas.DataFrame({'gender':1,'mutual_strength':0.9,'locations_together':14 ,'likes':34}, index=[0])

data = pandas.read_csv('csv/TrainingSet/test_train.csv', sep=',', na_values=".")
model = ols('response ~ gender + mutual_strength + locations_together * likes - locations_together - likes', data).fit()
summary.write(str(model.summary()))

x = model.predict(df)
print (x)

#y, X = patsy.dmatrices("response ~ gender + mutual_strength + locations_together + likes", data=data, return_type="dataframe")
#vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
#vif_file.write(str(vif))

