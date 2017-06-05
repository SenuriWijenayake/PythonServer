from googleplaces import GooglePlaces, types, lang
from pymongo import MongoClient

YOUR_API_KEY = 'AIzaSyCcIvxwR5NyiHdYHFAqgdTtEq9x7yP6VuU'
google_places = GooglePlaces(YOUR_API_KEY)

client = MongoClient('localhost', 27017)
db = client.script
locationPosts = db.locationPosts.find()
locations = db.locations
locations_collection = db.locations.find()

def get_place_details (name,lat,long):
    query_result = google_places.text_search(query=name, location="Sri Lanka", lat_lng={'lat':lat,'lng': long})
    count = 1
    for place in query_result.places:
        if (count is 1):
            count += 1
            place.get_details()
            my_place = {}
            my_place['name'] = name
            cood = place.geo_location
            my_place['longitude'] = float(cood['lng'])
            my_place['latitude'] = float(cood['lat'])
            my_place['id'] = place.place_id
            my_place['types'] = place.types
            if(place.rating is ''):
                my_place['rating'] = 3.0
            else:
                my_place['rating'] = float(place.rating)
            area = place.vicinity.split(',')
            length = len(area)
            my_place['area'] = area[length-1]
            return my_place

def get_all_locations_in_db():
    location_list = []
    for location in locations_collection:
        location_list.append(location['name'])
    return location_list

#Function to create location profiles for a given user based on his location posts
def create_location_profiles_for_user (user_id):
    #Extract the location Posts of the user
    record = db.locationPosts.find_one({'user_id' : user_id})
    #Get the list of locations in db
    location_exists = get_all_locations_in_db()
    for location in record['locations']:
        try:
            if (location['place']['name'] not in location_exists):
                details = get_place_details(location['place']['name'], location['place']['location']['latitude'], location['place']['location']['longitude'])
                if (details['name'] not in location_exists):
                    print ("Inserting location : " + details['name'])
                    db.locations.insert_one(details)
                    location_exists.append(details['name'])
                    location_exists.append(location['place']['name'])
        except Exception as e:
            print (e)
            pass
    print ("Completed creating profiles for " + user_id)






