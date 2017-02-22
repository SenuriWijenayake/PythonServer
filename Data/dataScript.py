from users import *
import simplejson as json

new_locations = []

#Script to create dummy location profiles
"""for item in rawLoc:
    
    x = randint(0,5)
    new_locations.append({
        
        "place_id": item + str(x),
        "name": item + str(x),
        "rating": randint(0,5)
    })
    new_locations.append({
        
        "place_id": item + str(x + 1),
        "name": item + str(x + 1),
        "rating": randint(0,5)
    })
    new_locations.append({
        
        "place_id": item + str(x + 2),
        "name": item + str(x + 2),
        "rating": randint(0,5)
    })
"""

#Sciprt to create dummy users
"""for x in range (50):
    new_locations.append({
        
        "user_id": str(x),
        "name": "User" + str(x)
    })
"""
"""
#Sciprt to create dummy preferences
final = []

for user in users:
    prefs = []
    indices = sample(range(0,49), 30)
    
    for index in indices:
        prefs.append({"place_id":locations[index]['id'], "rating": randint(1,5)})
        
    final.append({"user_id":user['id'], "prefs": prefs})
"""

#Function to create dummy friend lists for users based on similar schools and region
def createFriendLists():
    all_lists = []
    for active in users:
        friendList = []
        if ('education' in active and 'hometown' in active):
            for other in users:
                if ('education' in other and 'hometown' in other) and (other['id'] is not active['id']) and (other['hometown'] == active['hometown'] or other['education'] == active['education']):
                    friendList.append(other['id'])
            all_lists.append({"id":active['id'], "friends" : friendList})

    with open('friends.py', 'w') as f:
        json.dump(all_lists, f)

createFriendLists()


