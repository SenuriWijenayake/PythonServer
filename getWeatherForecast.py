import pyowm

api_keys = ['d32af81fbf749c1f469b1e762b35253a','e49703a5b52ce7508fff34fbbc803f6b','6b6d929a1dc81b448fb09ea0c0a99865','711267ec959c9f3170fb73c580ad2a15']
owm = pyowm.OWM(api_keys[0])

def get_weather_forecast(city,hours):

    forecast = owm.daily_forecast(city + ",lk")
    now = pyowm.timeutils.now()

    if(hours == 3):
        req_time = pyowm.timeutils.next_three_hours(now)
    if(hours == 6):
        three_hours = pyowm.timeutils.next_three_hours(now)
        req_time = pyowm.timeutils.next_three_hours(three_hours)


    start_forecast = forecast.will_be_sunny_at(now)
    end_forecast = forecast.will_be_sunny_at(req_time)

    if(start_forecast == False or end_forecast == False):
        return "rainy"
    else:
        return "sunny"


x = get_weather_forecast("Colombo",3)
print (x)


