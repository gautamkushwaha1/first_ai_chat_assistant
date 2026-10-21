from datetime import datetime , date
import requests

def get_current_time():
  return datetime.now().strftime(" %B %d , %Y at %I:%M %p")

def get_current_date():
  return date.today()

def get_city_weather(city):
  url = f"https://wttr.in/{city}?format=3"
  response = requests.get(url,timeout = 10)
  return response.text

Tools = [
  {
    "type" : "function",
    "function" : {
      "name" : "get_current_time",
      "description" : "Returns the current time ",
      "parameters" : {"type" : "object" , "properties" : {}}
    }
  },
  {
    "type":"function",
    "function":{
      "name":"get_current_date",
      "description":"Return the current date ",
      "parameters":{"type":"object","properties":{}}
    }
  },
  {
    "type":"function",
    "function":{
      "name":"get_city_weather",
      "description":"Returns the current weather to the given city",
      "parameters":{
        "type":"object",
        "properties":{
          "city":{
            "type":"string",
            "description":"city to get the weather forcast"
          }
        }
      }
    }
  }
]

fuction_name_to_function_map = {
  "get_current_time" : get_current_time,
  "get_current_date":get_current_date,
  "get_city_weather":get_city_weather
}
