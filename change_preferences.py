#Creating the database connection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.script

#Function to include the google place id in preferences
def include_google_id():
    preferences = db.preferences.find()
    for user in preferences:
        my_prefs = {}

        user_id = user['user_id']
        locs_rated = user['prefs']

        my_prefs['user_id'] = user_id
        my_prefs['prefs'] = []

        posts = db.locationPosts.find_one({'user_id':user_id})

        #For each preference
        for item in locs_rated:
            post_id = item['post_id']
            #Find the location post
            try:
                for post in posts['locations']:
                    if(post_id == post['post_id']):
                        #Create a new preference object
                        rating = float(item['rating'])
                        loc_profile = db.locations.find_one({'name':item['name']})
                        my_prefs['prefs'].append({
                            "post_id": item['post_id'],
                            "rating": rating,
                            "place_id": item['place_id'],
                            "name": item['name'],
                            "google_place_id" : loc_profile['id'],
                            "location" : {'lng': loc_profile['longitude'] , 'lat': loc_profile['latitude']}
                        })
            except TypeError as e:
                print (e)
                print (user_id)
                continue

        db.newPreferences.insert(my_prefs)


include_google_id()
