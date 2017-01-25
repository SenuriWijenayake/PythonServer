db = connect('127.0.0.1:27017/data');

function createUsers(){
	db.users.insert(
	   [
	     {"id": "1", "name": "Senuri Wijenayake", "age":24, "hometown":"Colombo", "gender":"Female"},
	     {"id": "2", "name": "Shashini Wije", "age":22, "hometown":"Colombo", "gender":"Female"},
	     {"id": "3", "name": "Sachini Chathurika", "age":25, "hometown":"Galle", "gender":"Female"},
	     {"id": "4", "name": "Amal Perera", "age":30, "hometown":"Kandy", "gender":"Male"},
	     {"id": "5", "name": "Janitha Chanuka", "age":24, "hometown":"Galle", "gender":"Male"},
	     {"id": "6", "name": "Ema Watson", "age":32, "hometown":"Kandy", "gender":"Female"},
	     {"id": "7", "name": "Kasun Perera", "age":21, "hometown":"Colombo", "gender":"Male"}
	   ]
	);
}

function createLocations(){
	db.locations.insert(
	   [
	     {"id": "21", 
	     "name": "Kandy City Centre, Sri Dalada Veediya, Kandy, Sri Lanka", 
	     "placeId" : "ChIJf8zC4Ctm4zoRl_Rm2uP_2Q8",
	     "geometry": {
	      "location": {
	        "lat": 7.292331299999999,
	        "lng": 80.637017
	      },
	      "viewport": {
		       "northeast": {
		          "lat": 7.2934581,
		          "lng": 80.63703349999999
		        },
		      "southwest": {
		          "lat": 7.291955699999999,
		          "lng": 80.6369675
		        }
	       }
	    },
    	"icon": "https://maps.gstatic.com/mapfiles/place_api/icons/geocode-71.png", 
  		"rating" : 4,
  		"description" : "This is a comment about the KCC",
  		"category" : "Entertainment"
  		},

  		{"id": "22", 
	     "name": "Kandy Lake, Kandy, Central Province, Sri Lanka",
	     "placeId" : "", 
	     "geometry": {
	      "location": {
	        "lat": 7.292331299999999,
	        "lng": 80.637017
	      },
	      "viewport": {
		       "northeast": {
		          "lat": 7.2934581,
		          "lng": 80.63703349999999
		        },
		      "southwest": {
		          "lat": 7.291955699999999,
		          "lng": 80.6369675
		        }
	       }
	    },
    	"icon": "https://maps.gstatic.com/mapfiles/place_api/icons/geocode-71.png", 
  		"rating" : 4,
  		"description" : "This is a comment about the KCC",
  		"category" : "Entertainment"
  		},
	   ]
	);
}