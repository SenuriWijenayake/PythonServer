#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.data
userPrefs = db.userPrefs.find_one({},{"_id":0})


