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
from requests import get



class myThread (threading.Thread):
   def __init__(self, name,email):
      threading.Thread.__init__(self)
      self.name = name
      self.email = email

   def getWeatherByLoc(self):
      try:
         ip = get('https://api.ipify.org').text

         ip_address = ip
         request_url = 'https://geolocation-db.com/jsonp/' + ip_address
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

         # Weather API
         api = (
         "https://api.openweathermap.org/data/2.5/onecall?lat=38.7267&lon=-9.1403&exclude=current,hourly,minutely,alerts&units=metric&appid=a0436779bfc4457741c32fb931a75148"
         )
         json_data = requests.get(api).json()

         temperature = []
         feels_likeArray = []
         descripArray = []
         json_data = json_data["daily"]

         for i in range(7):
            temperature.append(json_data[i]["temp"]["day"])
            feels_likeArray.append(json_data[i]["weather"][0]["main"])
            descripArray.append(json_data[i]["weather"][0]["description"])


         OutputString = """From: Temp Sender <from@fromdomain.com>
         To: me <to@todomain.com>
         Subject: Admission Done

         """ 

         for i in range(7):
            OutputString += """\n Temperature for day """  + str(i ) + """ """ + str(temperature[i])
            OutputString +=  """ \n Feels Like,  """  + str(feels_likeArray[i])
            OutputString +=  """ \n So there will be """  + str(descripArray[i]) + """ \n"""

         return OutputString
      except Exception as e:
         print("error",e)



   def run(self):
      print ("Starting " + self.name)
      test = 0
      numberOfTimes = 1
      while(True):
         if test < numberOfTimes:
            for m in self.email:
               dataArray = self.getWeatherByLoc()
               message(m, dataArray)
         else: break
         test = test + 1
         time.sleep(1)
      print( "Exiting " + self.name)



class appThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      print ("Starting " + self.name)
      import weather2
      print( "Exiting " + self.name)

thread1 = myThread("Thread-1" , ("20104034.chirag.padyal@gmail.com", "rohanahire100@gmail.com","prathambhagwat4214@gmail.com"))
thread1.start()

# To run this thread call this thread in another file
# from thread_bg import myThread
# thread1 = myThread("Thread-1" , ("rohanahire100@gmail.com"))
# thread1.start()