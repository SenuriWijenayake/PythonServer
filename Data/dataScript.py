from locations import *
from users import *
from random import *
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

#Sciprt to create dummy preferences
final = []

for user in users:
    prefs = []
    indices = sample(range(0,49), 30)
    
    for index in indices:
        prefs.append({"place_id":locations[index]['id'], "rating": randint(1,5)})
        
    final.append({"user_id":user['id'], "prefs": prefs})
    
with open('prefs.py', 'w') as f:
    json.dump(final, f)

    

    