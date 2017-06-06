import facebook
import requests
import simplejson as json

access_token='EAACEdEose0cBAFaIbQn4ZAa3wpSa5uH3FjWEVkd16rm1UC8UAZC2N6mmGDMFJiJd9NyZA3YDiKZBbWa6qO83XYVjJ9mREudPMY9pi0mDAhwetikvPc4UOlx67oZBZCv3mp0eKnmIgPFXefR8vIlZCmtEGZBjWDE2oV0fhoGQl13mSi5k3O5FJems8JKGHvkiKcIZD'

user = '1665852693730402'

graph = facebook.GraphAPI(access_token, version='2.7')

profile = graph.get_object(user, fields = 'id,name,birthday,age_range,education,hometown,location,gender,religion')
feed = graph.get_connections(profile['id'], 'feed')
my_feed = graph.get_connections(profile['id'], 'feed', **{'fields':'place'})
friends = graph.get_connections(id='me', connection_name='friends')
tagged_places = graph.get_connections(profile['id'], 'tagged_places')

all_friends = []
full_feed = []
loc_tags = {}
num_extract = 0

#Extract user profile
print ("Downloading the user's public profile")
with open('profile.json', 'w') as f:
    json.dump(profile, f)

print("Analyzing your profile to determine tagged places..")
#Determine how many location posts to be extracted to gave 50 locations
while True:
    try:
        for loc in tagged_places['data']:
            if(loc_tags.__len__() < 50):
                if (loc['place']['id'] not in loc_tags.keys()):
                    loc_tags[loc['place']['id']] = 1
                else:
                    loc_tags[loc['place']['id']] += 1
        tagged_places = requests.get(tagged_places['paging']['next']).json()

    except KeyError:
        break

tot_posts = sum(loc_tags.values())
print ("You have " + str(loc_tags.__len__())  + " number of locations visited")

print ("You have " + str(tot_posts)  + " number of location posts to be extracted")
print ("Please be patient while the details are been extracted..")

num = 0
loc_posts = []

should_repeat = 1
#Extract the location tagged post ids corresponding to the 50 locations
while True:
    try:
        for post in my_feed['data']:
            #Check if the post has a place tag
            if ('place' in post):
                num += 1
                print ("Progress (id extraction) : " + str(int(num/tot_posts*100)) + "%")
                loc_posts.append({'post_id' : post['id'], 'place_id': post['place']['id'], 'name' : post['place']['name'], 'rating' : ''})
                if(num >= tot_posts):
                    should_repeat = 0
                    break

        if(should_repeat):
            my_feed = requests.get(my_feed['paging']['next']).json()
        else:
            raise KeyError

    except KeyError:
        break

print ("The posts ids were successfully extracted!")
print ("Extraction of the posts now initiaiting..")

#Get the distinct locations to rate
location_ratings = []
distint_ids = []
ids = []

for item in loc_posts:
    if(item['place_id'] not in distint_ids):
        distint_ids.append(item['place_id'])
        ids.append(item['post_id'])
        location_ratings.append(item)

#Extract the posts
location_feed_posts = []
countx = 0
total = distint_ids.__len__()

for id in ids:
    try:
        location_feed_posts.append(graph.get_object(id, fields = 'id,from,to,created_time,type,story,likes,place,comments,with_tags,message,reactions'))
        countx += 1
        print ("Progress (location_tags): " + str(int(countx/total*100)) + "%")

    except facebook.GraphAPIError:
        continue

loc_output = {}
loc_output['user_id'] = user
loc_output['locations'] = location_feed_posts

with open('location_posts.json', 'w') as f:
    json.dump(loc_output, f)

print (str(location_feed_posts.__len__()) + " posts were successfully collected")

print ("Lets now rate the locations you have visited! Please enter a rating between 1-5")
print ("1 : Poor")
print ("2 : Fair")
print ("3 : Good")
print ("4 : Very Good")
print ("5 : Excellent")

#Get the user's explicit rating for each location
for location in location_ratings:
     name = str(location['name'].encode("utf-8"))
     value = input("Rate (1-5) your experience at " + name + " : ")
     location['rating'] = value

rating_output = {}
rating_output['user_id'] = user
rating_output['prefs'] = location_ratings

with open('ratings.json', 'w') as f:
    json.dump(rating_output, f)
print ("Location ratings successfully stored!")

#Get the friend list of the user
while True:
    try:
        for friend in friends['data']:
            all_friends.append(friend)
        friends = requests.get(friends['paging']['cursor']['next']).json()

    except KeyError:
        break

print ("You have " + str(all_friends.__len__()) + " friends using the application")
print ("Successfully extracted your friend list!")

friend_output = {}
friend_output['user_id'] = user
friend_output['friends'] = all_friends
friend_output['total_count'] = friends['summary']['total_count']

with open('friends.json', 'w') as f:
    json.dump(friend_output, f)

print ("Accessing the public feed. Please be patient..")
#Get the feed of the user

number_of_posts = 500
counts = 0
repeat = 1

while True:
    try:
        for post in feed['data']:
            full_feed.append(post['id'])
            counts += 1
            if(counts >= number_of_posts):
                repeat = 0
                break

        if(repeat):
            feed = requests.get(feed['paging']['next']).json()
        else:
            raise KeyError

    except KeyError:
        break

len = full_feed.__len__()
print ("The most recent " + str(len) + " posts are been extracted. Please be patient until completion..")

feed_arr = []
count = 0

for id in full_feed:
    try:
        feed_arr.append(graph.get_object(id, fields = 'id,from,to,created_time,type,story,likes,place,comments,with_tags,message,reactions'))
        count += 1
        print ("Progress (feed) : " + str(int(count/number_of_posts*100)) + "%")

    except facebook.GraphAPIError:
        continue

feed_output = {}
feed_output['user_id'] = user
feed_output['feed'] = feed_arr

with open('feed.json', 'w') as f:
    json.dump(feed_output, f)
print ("Posts were successfully collected")

