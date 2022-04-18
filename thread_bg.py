import threading
import time
from smtp import message
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import socket

import pytz
from datetime import datetime

import requests
import json


class myThread (threading.Thread):
   def __init__(self, name,email):
      threading.Thread.__init__(self)
      self.name = name
      self.email = email

   def getWeatherByLoc(self):
      try:
         host_name = socket.gethostname()
         host_ip = socket.gethostbyname(host_name)
         ip_address = host_ip
         request_url = 'https://geolocation-db.com/jsonp/' + ip_address
         # Send request and decode the result
         response = requests.get(request_url)
         result = response.content.decode()
         # Clean the returned string so it just contains the dictionary data for the IP address
         result = result.split("(")[1].strip(")")
         # Convert this data into a dictionary
         result  = json.loads(result)

         city = result['city']
         # print(result['city'])

         geolocator = Nominatim(user_agent="geoapiExercises")
         location = geolocator.geocode(city)
         obj = TimezoneFinder()
         result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
         home = pytz.timezone(result)
         local_time = datetime.now(home)
         current_time = local_time.strftime("%I:%M %p")

         # clock.config(text=current_time)
         # name.config(text="CURRENT TIME")
         # print(result)

         # Weather API
         api = (
            "https://api.openweathermap.org/data/2.5/weather?q="
            + city
            + "&appid=a0436779bfc4457741c32fb931a75148"
         )
# https://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=a0436779bfc4457741c32fb931a75148
         json_data = requests.get(api).json()
         # condition = json_data["weather"][0]["main"]
         description = json_data["weather"][0]["description"]
         tempt = int(json_data["main"]["temp"] - 273.15)
         feels_like = int(json_data["main"]["feels_like"] - 273.15)
         press = json_data["main"]["pressure"]
         humid = json_data["main"]["humidity"]
         wind_1 = json_data["wind"]["speed"]

         # return [condition,description,tempt,feels_like,press,humid,wind_1,current_time, city]
         return [str(current_time),str(city),str(tempt),str(wind_1),str(humid),str(press),str(feels_like),str(description)]
      except Exception as e:
      #   messagebox.showerror("Weather App", "Invalid Input!")
         print("error",e)



   def run(self):
      print ("Starting " + self.name)
      timeout = time.time()

      test = 0
      while(True):
         for m in self.email:
            dataArray = self.getWeatherByLoc()
            # dataArray = ["5","6","7","5","6","7","8","9"]
            if test == 5 or time.time() > timeout:
               break
            test = test + 1
            time.sleep(60)
            message(m, dataArray)
      print( "Exiting " + self.name)



class appThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      print ("Starting " + self.name)
      import weather2
      print( "Exiting " + self.name)

thread1 = myThread("Thread-1" , ("kadamchirag232001@gmail.com", "rohanahire100@gmail.com","prathambhagwat4214@gmail.com"))
thread1.start()







# # Create new threads
# thread1 = myThread("Thread-1" , ("kadamchirag232001@gmail.com", "chiragkadam77@gmail.com","20104034.chirag.padyal@gmail.com","freakstar03@gmail.com"))
# thread2 = myThread("Thread-2")

# Start new Threads
# thread1.start()
# # thread2.start()

# print ("Exiting Main Thread")