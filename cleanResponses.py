from pymongo import MongoClient
from crud import *
from networkSimilarityMeasurements import *

client = MongoClient('localhost', 27017)
db = client.script

raw_responses = db.responses_raw.find()
responses = db.responses
friends = list(db.friends.find())

def findResponsesOfUser (active):
    res = db.responses_raw.find({'active':active})
    my_resposes = {}
    for response in list(res):
        res = {'1' : int(response['Q1']),
               '2' : int(response['Q2']),
               '3' : int(response['Q3']),
               '4' : int(response['Q4'])
               }
        my_resposes[response['other']] = res
    responses.insert({'id': active, 'responses' : my_resposes })

#all_users = getAllUsers()
#for user in list(all_users):
#    findResponsesOfUser(user['id'])

#Function to combine the data and create a csv file
def createCSV():
    users = list(db.networkSims.find())

    arr = []
    for user in users:

        active = user['id']
        sims = user['similarities']
        for otr in sims:

            #Find the corresponsing response record
            other = sims[otr]
            response = db.responses_raw.find_one({'active':active, 'other': otr})

            if(response is not None):
                friends = db.friends.find_one({'id':active},{'_id':0})
                profile = profile_similarity(active,str(otr))
                mutual_strength = other['mutuals_distinct_friends']['mutuals'] / len(friends['friends'])

                comments = int(other['num_likes_comments_in']['comments']) + int(other['num_likes_comments_out']['comments'])
                likes = other['num_likes_comments_in']['likes'] + other['num_likes_comments_out']['likes']

                last_comm = other['last_communication']
                if (last_comm == -1):
                    last_comm = 100
                elif (last_comm < -1):
                    last_comm = last_comm + 6

                object = {
                    'id': active + "_" + str(otr),
                    'wall_words': other['wall_words'],
                    'locations_together' : other['appearence in photos']['location_count'],
                    'photos_together' : other['appearence in photos']['photo_count'],
                    'last_comm' : last_comm,
                    'likes' : likes,
                    'comments' : comments,
                    'mutuals' : other['mutuals_distinct_friends']['mutuals'],
                    'posts' : other['inbound_posts'] + other['outbound_posts'],
                    'user_friends': len(friends['friends']),
                    'total_friend_count' : friends['total_count'],
                    'mutual_strength': mutual_strength,
                    'age_gap' : profile['age_gap'],
                    'religion' : profile['religion'],
                    'gender' : profile['gender'],
                    'profile_sim' : profile['profileSim']
                }

                objectOne = object.copy()
                objectTwo = object.copy()
                objectThree = object.copy()
                objectFour = object.copy()

                objectOne['response'] = response['Q1']
                objectTwo['response'] = response['Q2']
                objectThree['response'] = response['Q3']
                objectFour['response'] = response['Q4']

                db.question_one.insert(objectOne)
                db.question_two.insert(objectTwo)
                db.question_three.insert(objectThree)
                db.question_four.insert(objectFour)

#createCSV()

#Function to find friends
def find_friends(active):
    print ("New User" + active)
    friends_found = []
    for user in friends:
        if (active in user['friends']):
            friends_found.append(user['id'])

    my_list = db.friends.find_one({'id':active},{'_id':0,'friends':1})
    for id in friends_found:
        if (id not in my_list['friends']):
            print ("Id not found : " + id)

