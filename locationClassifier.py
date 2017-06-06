import nltk
from pymongo import MongoClient

#Initliaze the database connection
client = MongoClient("localhost", 27017)
db = client.script

original = db.locationClassifier
data = list(original.find())
types = ['aquarium','airport','point_of_interest','establishment','amusement_park','aquarium','art_gallery','lodging','bar','food',
         'restaurant','cafe','shopping_mall','place_of_worship','church','health','spa','bowling_alley','casino','park', 'hindu_temple',
         'mosque','library','liquor_store','movie_theater','museum','night_club','stadium','zoo']


#Function to change the training data set to the format required
def regression_function(train,label):
    result={}
    for t in types:
        if(t in train):
            value = 1
        else:
            value = 0
        result[t] = value
    return(result,label)


#Function to extract the training set from the database
def create_training_set():
    train = []
    for item in data:
        label = item['in_out']
        types = item['types']
        res = regression_function(types,label)
        train.append(res)

    return train


#Function to convert a new location to the matrix required
def changeFromat(location):
    my_types = location['types']
    result={}
    for u in types:
        if(u in my_types):
            value = 1
        else:
            value = 0
        result[u] = value
    return (result)



#Function to classify an array of locations as indoor or outdoor
#Indoor returns 1
#Outdoor returns 0
def classifyLocations(locations,train):

    classifier = nltk.classify.NaiveBayesClassifier.train(train)
    output = {}
    for loc in locations:
        #Change the format to the required format
        output[loc['id']] = changeFromat(loc)

    for key in output:
        #Call the classifier
        output[key] = classifier.classify(output[key])
    return output



