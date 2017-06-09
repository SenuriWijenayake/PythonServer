import pyowm

api_keys = ['d32af81fbf749c1f469b1e762b35253a','e49703a5b52ce7508fff34fbbc803f6b','6b6d929a1dc81b448fb09ea0c0a99865','711267ec959c9f3170fb73c580ad2a15']
owm = pyowm.OWM(api_keys[1])

def get_weather_forecast(lat,lng,hours):
    #Include start time
    city = str(get_city(lat,lng))
    #city = "Colombo"
    forecast = owm.daily_forecast(city + ",lk")
    if(forecast is None):
        forecast = owm.daily_forecast("Colombo" + ",lk")
    now = pyowm.timeutils.now()
    print (now)

    three_hours = pyowm.timeutils.next_three_hours(now)
    six_hours = pyowm.timeutils.next_three_hours(three_hours)
    nine_hours = pyowm.timeutils.next_three_hours(six_hours)
    twelve_hours = pyowm.timeutils.next_three_hours(nine_hours)

    start_forecast = forecast.will_be_sunny_at(now)
    three_forecast = forecast.will_be_sunny_at(three_hours)
    six_forecast = forecast.will_be_sunny_at(six_hours)
    nine_forecast = forecast.will_be_sunny_at(nine_hours)
    twelve_forecast = forecast.will_be_sunny_at(twelve_hours)

    if (hours == 3):
        if (start_forecast == False or three_forecast == False):
            return "rainy"
        else:
            return "sunny"

    if (3 < hours <= 6):
        if (start_forecast == False or three_forecast == False or six_forecast == False):
            return "rainy"
        else:
            return "sunny"

    if (6 < hours <= 9):
        if (start_forecast == False or three_forecast == False or six_forecast == False or nine_forecast == False):
            return "rainy"
        else:
            return "sunny"

    if (9 < hours <= 12):
        if (start_forecast == False or three_forecast == False or six_forecast == False or nine_forecast == False or twelve_forecast == False):
            return "rainy"
        else:
            return "sunny"

def get_city(lat,lng):
    obs_list = owm.weather_around_coords(lat,lng)
    obs = obs_list[0]
    l = obs.get_location()
    return (l.get_name())



