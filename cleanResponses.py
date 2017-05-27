from pymongo import MongoClient
from crud import *

client = MongoClient('localhost', 27017)
db = client.script

raw_responses = db.responses_raw.find()
responses = db.responses

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
                arr.append (active + "_" + otr)
                print (len(arr))
                comments = int(other['num_likes_comments_in']['comments']) + int(other['num_likes_comments_out']['comments'])
                likes = other['num_likes_comments_in']['likes'] + other['num_likes_comments_out']['likes']
                friends = db.friends.find_one({'id':active},{'_id':0,'friends':1})

                object = {
                    'id': active + "_" + str(otr),
                    'wall_words': other['wall_words'],
                    'locations_together' : other['appearence in photos']['location_count'],
                    'photos_together' : other['appearence in photos']['photo_count'],
                    'last_comm' : other['last_communication'],
                    'likes' : likes,
                    'comments' : comments,
                    'mutuals_distinct' : round(other['mutuals_distinct_friends']['mutuals'] / len(friends['friends'])),
                    'posts' : other['inbound_posts'] + other['outbound_posts'],
                    'user_friends': len(friends['friends'])
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
