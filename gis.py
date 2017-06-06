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

key = 'AIzaSyA7PJ6wBe_w3lC6KPIYvQ5s-F5ZfALU7uA'

def get_rated_locations(user,lat,lng,hours,radius,training_data,avgs,all_sims,location_train_set):
    mix_of_locations = []
    mix_keys = []

    #Get a mix of locations nearby which are open and within the radius
    food = get_restaurants_cafes_food(key,lat,lng,radius)
    lodging = get_hotels_lodging(key,lat,lng,radius)
    parks = get_fun_parks_zoos_places(key,lat,lng,radius)
    religious = get_religious_places(key,lat,lng,radius)
    indoor_boring = get_boring_indoor_places(key,lat,lng,radius)
    indoor_fun = get_cool_indoor_places(key,lat,lng,radius)

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

    #Get the weather forecast for the trip duration
    weather = get_weather_forecast(lat,lng,hours)

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
        final_locations.append(object)
    return final_locations


def get_restaurants_cafes_food(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=restaurant|food|cafe&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:10]
        return (top_ten)
    else:
        return []


def get_hotels_lodging(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=lodging&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:10]
        return (top_ten)
    else:
        return []


def get_fun_parks_zoos_places(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=amusement_park|park|zoo&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:10]
        return (top_ten)
    else:
        return []


def get_religious_places(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=church|place_of_worship|mosque|hindu_temple&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:10]
        return (top_ten)
    else:
        return []


def get_boring_indoor_places(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=aquarium|art_gallery|museum|movie_theater|library&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:]
        return (top_ten)
    else:
        return []


def get_cool_indoor_places(key,lat,lng,radius):
    response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) + "," + str(lng) + "&radius=" + str(radius) + "&types=bar|casino|spa|shopping_mall|night_club|movie_theater&key=" + key + "&opennow").read().decode('utf8')
    object = json.loads(response)
    if (len(object['results']) != 0):
        preprocessed = preprocess_google_response(object['results'])
        #Get the top ten based on location rating
        top_ten = preprocessed[0:20]
        return (top_ten)
    else:
        return []


def preprocess_google_response(object):
    response = []
    for obj in object:
        preprocessed = {}
        preprocessed['id'] = obj['place_id']

        areas = obj['vicinity'].split(",")
        area = areas[len(areas)-1].replace(" ","")

        preprocessed['area'] = area
        preprocessed['longitude'] = obj['geometry']['location']['lng']
        preprocessed['latitude'] = obj['geometry']['location']['lat']
        if('rating' in obj):
            preprocessed['rating'] = obj['rating']
        else:
            preprocessed['rating'] = 3.5
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



