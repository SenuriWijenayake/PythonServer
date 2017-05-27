#This includes the functions to calculate the network similarity between two users when they are already friends on facebook
from datetime import datetime
from similarities import *

#Predictive Variables
#Each of these functions should be run twice

#Outboud posts (participant initiated posts on the friend)
#Posts with the friend in tags + Posts in the friends feed with from by the user
def outbound_posts(active,other):
    active_feed = getFeedOfUser(active)
    other_feed = getFeedOfUser(other)

    #Get the names of the two users
    active_profile = getUserDetails(active)
    other_profile = getUserDetails(other)

    ac_name = active_profile['name'].split()
    ot_name = other_profile['name'].split()

    out_count = 0
    #extract the posts initiated by active on friend
    for post in other_feed['feed']:
        if(post['from']['id'] == active):
            out_count += 1

    #extract the posts on the feed of the user tagged with the friend
    for post in active_feed['feed']:
        if('with_tags' in post):
            for tag in post['with_tags']['data']:
                if (tag['id'] == other):
                    out_count += 1
                    break
        if('message' in post):
            index = post['message'].find(other_profile['name'])
            if (index != -1):
                out_count += 1
            else:
                index = post['message'].find(ot_name[0])
                if (index != -1):
                    out_count += 1

    return out_count

#Wall words exchanged interchanged as messages or comments are extracted
def wall_words(active,other):
    active_feed = getFeedOfUser(active)
    other_feed = getFeedOfUser(other)

    words = 0

    #Wall words by active and other in posts created by either of them on the active's feed
    for post in active_feed['feed']:
        if (post['from']['id'] == other or post['from']['id'] == active):
            if ('story' in post):
                words += len (post['story'].split())
            if ('message' in post):
                words += len(post['message'].split())
            #Consider the comments as well
            if ('comments' in post):
                for comment in post['comments']['data']:
                    if(comment['from']['id'] == active or comment['from']['id'] == other):
                        words += len(comment['message'].split())
    return words

#Number of comments by other on active
def comments_likes_by_friend(active,other):
    active_feed = getFeedOfUser(active)

    num_comments = 0
    num_likes = 0
    for post in active_feed['feed']:
        if ('comments' in post):
            for comment in post['comments']['data']:
                if (comment['from']['id'] == other):
                    num_comments += 1
        if ('likes' in post):
            for like in post['likes']['data']:
                if (like['id'] == other):
                    num_likes += 1

    return ({'comments':num_comments, 'likes':num_likes})

#Intensity Variables
#Last communication (posted,commented or liked etc)
def last_communication (active,other):
    date_collected = datetime.strptime('2017-03-31', '%Y-%m-%d')
    active_feed = getFeedOfUser(active)
    other_feed = getFeedOfUser(other)
    date = []
    for post in active_feed['feed']:
        if (post['from']['id'] == other):
            created_on = post['created_time'][0:10]
            date.append(created_on)
        if ('comments' in post):
            for comment in post['comments']['data']:
                if (comment['from']['id'] == other):
                    date.append(comment['created_time'][0:10])
        if ('likes' in post):
            for like in post['likes']['data']:
                if (like['id'] == other):
                    date.append(post['created_time'][0:10])

    if (len(date) == 0):
        return -1

    final_day = date[0]
    for day in date:
        if (day > final_day):
            final_day = day

    final_day = datetime.strptime(final_day, '%Y-%m-%d')
    days = (str(date_collected - final_day))[0:2]
    if (days == '0:'):
        return 0
    else:
        return int(days)


#Get the number of total friends on facebook
def get_friends_count(active):
    num = friends.find_one({"id":active},{"_id":0,"total_count":1})
    return num['total_count']


#Appearence together in photos
def appearence_in_photos_locations_together(active,other):
    active_feed = getFeedOfUser(active)

    location_tag_count = 0
    photo_tag_count = 0

    for post in active_feed['feed']:
        if (post['type'] == 'photo' and 'with_tags' in post):
            for tag in post['with_tags']['data']:
                if (tag['id'] == other):
                    photo_tag_count += 1

        if ('place' in post and 'with_tags' in post):
            for tag in post['with_tags']['data']:
                if (tag['id'] == other):
                    location_tag_count += 1

    return ({'photo_count':photo_tag_count, 'location_count':location_tag_count})


#Structural Variables
#Number of mutuals / number of distinct friends of both using this application
def mutuals_over_distinct_friends(active,other):
    mutuals = findMutuals (active,other)

    active_friends = getFriends(active)
    other_friends = getFriends(other)

    distinct_friends = []
    for friend in active_friends['friends']:
        if (friend not in distinct_friends):
            distinct_friends.append(friend)

    for friend in other_friends['friends']:
        if (friend not in distinct_friends):
            distinct_friends.append(friend)

    mutual_count = len(mutuals)
    distinct_count = len(distinct_friends)

    return ({'mutuals':mutual_count , 'distinct':distinct_count})



#Function to calculate the above measures for all users who are friends of one another
def calculateNetworkMeasurements():
    all_users = list(getAllUsers())
    all_sims = {}
    count = 0
    for user in all_users:
        count += 1
        active = user['id']
        my_sims = {}
        #Get the user's friends
        my_friends = getFriends(active)
        for other in my_friends['friends']:
            sim_for_friend = {
                'outbound_posts': outbound_posts(active,other),
                'inbound_posts' : outbound_posts(other,active),
                'wall_words': int(wall_words(active,other)) + int(wall_words(other,active)),
                'num_likes_comments_out' : comments_likes_by_friend(active,other),
                'num_likes_comments_in' : comments_likes_by_friend(other,active),
                'last_communication': last_communication(active,other),
                'friend_count' : get_friends_count(active),
                'appearence in photos' : appearence_in_photos_locations_together(active,other),
                'mutuals_distinct_friends' : mutuals_over_distinct_friends(active,other)
            }
            my_sims[other] = sim_for_friend
        #all_sims[active] = my_sims
        db.networkSims.insert({'id':active, 'similarities' : my_sims})
        print (count)
    return all_sims


