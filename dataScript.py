from locations import *
from users import *
from random import *
import simplejson as json

new_locations = []

#Script to create dummy location profiles
"""for item in locations:
    
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

for user in users:
    prefs = []
    for loc in locations:
        prefs.append({
            "location_id": loc['place_id'],
            "rating": randint(0,5)
        })

    new_locations.append({
        "user_id": user['user_id'],
        "prefs": prefs
    })
        
with open('userPrefs.py', 'w') as f:
    json.dump(new_locations, f)
    

    