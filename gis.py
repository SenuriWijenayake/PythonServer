#This script is used to connect the weather api, location classifier and the recommendation module
#Android client will give the user_id and the current location of the user, the trip duration and the radius to be covered
#Output is the rated locations

import urllib.request
import json
from operator import itemgetter
from locationClassifier import classifyLocations
from getWeatherForecast import get_weather_forecast
from rateLocations import rateLocations
from startup import *

client = MongoClient('localhost', 27017)
db = client.script

key = 'AIzaSyA7PJ6wBe_w3lC6KPIYvQ5s-F5ZfALU7uA'
considered_types = ['amusement_park','aquarium','art_gallery','bakery','bar','cafe','casino',
                    'church','clothing_store','hindu_temple','library','lodging','mosque','movie_theater',
                    'museum','night_club','park','place_of_worship','restaurant','shopping_mall','spa','university','zoo']

#def get_rated_locations(user,lat,lng,hours,start,radius,training_data,avgs,all_sims,location_train_set)
def get_rated_locations(user,lat,lng,hours,start,radius,training_data,avgs,all_sims,location_train_set):
    mix_of_locations = []
    mix_keys = []

    #Get the weather forecast for the trip duration
    weather,city = get_weather_forecast(lat,lng,hours,start)
    #weather = "rainy"

    #Get a mix of locations nearby which are open and within the radius
    food = get_restaurants_cafes_food(key,lat,lng,radius,city)
    lodging = get_hotels_lodging(key,lat,lng,radius,city)
    parks = get_fun_parks_zoos_places(key,lat,lng,radius,city)
    religious = get_religious_places(key,lat,lng,radius,city)
    indoor_boring = get_boring_indoor_places(key,lat,lng,radius,city)
    indoor_fun = get_cool_indoor_places(key,lat,lng,radius,city)

    if (len(food) != 0):
        for place in food:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)
    if (len(lodging) != 0):
        for place in lodging:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)
    if (len(parks) != 0):
        for place in parks:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)
    if (len(religious) != 0):
        for place in religious:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)
    if (len(indoor_boring) != 0):
        for place in indoor_boring:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)
    if (len(indoor_fun) != 0):
        for place in indoor_fun:
            if(place['id'] not in mix_keys):
                mix_keys.append(place['id'])
                mix_of_locations.append(place)


    if(weather == 'rainy'):
        #Select only indoor places
        #This is when we need to use the classifier
        classified_locations = classifyLocations(mix_of_locations,location_train_set)

        #Out of the classified locations filter out the indoor locations
        filtered_locations = filter_indoor_locations(classified_locations,mix_of_locations)

    else:
        #No need to call the classifier. All locations can be visited
        filtered_locations = mix_of_locations

    #Next rate the locations
    rated_locations, location_list = rateLocations(training_data,user,filtered_locations,avgs,all_sims)
    final_locations = []
    for location in filtered_locations:
        object = {
            'id' : location['id'],
            'rating' : rated_locations[location['id']],
            'name' : location['name'],
            'latitude' : location['latitude'],
            'longitude' : location['longitude']
        }
        if ('photos' in location):
            object['photos'] = location['photos']
        final_locations.append(object)

    return (final_locations)


def get_restaurants_cafes_food(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=restaurant|food|cafe&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 0
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['restaurant','cafe'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:3]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def get_hotels_lodging(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=lodging&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 0
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['lodging'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:2]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def get_fun_parks_zoos_places(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=amusement_park|park|zoo&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 0
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['park','zoo'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:2]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def get_religious_places(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=church|place_of_worship|mosque|hindu_temple&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 1
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['place_of_worship','church','hindu_temple','mosque'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:3]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def get_boring_indoor_places(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=aquarium|art_gallery|museum|movie_theater|library&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 0
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['art_gallery','museum','movie_theater','library'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:3]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def get_cool_indoor_places(key,lat,lng,radius,city):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=bar|casino|spa|shopping_mall|night_club|movie_theater&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    flag = 0
    popular_places = []
    if(city.lower() in tourist_cities):
        popular_places = extract_locations_for_city(city,['bar','casino','shopping_mall','movie_theater'])

    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'],flag)
        #Get the top ten based on location rating
        top_ten = preprocessed[0:3]
        for item in top_ten:
            popular_places.append(item)

        return (popular_places)
    else:
        return (popular_places)


def preprocess_google_response(object,flag):
    response = []
    if (flag == 0):
        for obj in object:
            if ('rating' in obj and 'types' in obj):
                    preprocessed = {}
                    preprocessed['id'] = obj['place_id']

                    areas = obj['vicinity'].split(",")
                    area = areas[len(areas)-1].replace(" ","")

                    preprocessed['area'] = area
                    preprocessed['longitude'] = obj['geometry']['location']['lng']
                    preprocessed['latitude'] = obj['geometry']['location']['lat']
                    preprocessed['rating'] = obj['rating']
                    preprocessed['name'] = obj['name']

                    if ('photos' in obj):
                        preprocessed['photos'] = obj['photos']
                    preprocessed['types'] = obj['types']

                    response.append(preprocessed)

    if (flag == 1):
        for obj in object:
            if ('types' in obj):
                    preprocessed = {}
                    preprocessed['id'] = obj['place_id']

                    areas = obj['vicinity'].split(",")
                    area = areas[len(areas)-1].replace(" ","")

                    preprocessed['area'] = area
                    preprocessed['longitude'] = obj['geometry']['location']['lng']
                    preprocessed['latitude'] = obj['geometry']['location']['lat']

                    if ('rating' in obj):
                        preprocessed['rating'] = obj['rating']
                    else:
                       preprocessed['rating'] = 3

                    preprocessed['name'] = obj['name']

                    if ('photos' in obj):
                        preprocessed['photos'] = obj['photos']
                    preprocessed['types'] = obj['types']

                    response.append(preprocessed)



    new_list = sorted(response, key=itemgetter('rating'), reverse=True)
    return new_list


def filter_indoor_locations(locations,mix_of_locations):
    filtered = []
    for item in locations:
        if(locations[item] == 1):
            filtered.append(item)

    final = []
    for location in mix_of_locations:
        if(location['id'] in filtered):
            final.append(location)

    return final



tourist_cities = ['colombo','galle','matara','kandy','trincomalee','nuwaraeliya','badulla','polonnaruwa','anuradhapura','kataragama']
def get_good_locations_from_collection(city):
    city_lower = city.lower()
    if(city_lower in tourist_cities):
        city_title = city_lower.title()
        results = list(extract_locations_for_city(city_title))
    return results



def extract_locations_for_city(city,types):
    results = list(db.touristLocations.find({'area':city, 'types': { '$in' : types}},{'_id':0}).sort([("rating", -1)]))
    final = []
    for res in results:
        if('types' in res):
            final.append(res)
    return final[0:2]


#x = get_rated_locations("1665852693730402",6.9271,79.8612,6,"2017-06-10-12-0",5000,training_data,avgs,all_sims,location_train_set)
#print (x)
