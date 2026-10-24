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

def get_current_city():
  return "delhi"

Tools = [

  {
    "type" : "function",
    "function" : {
      "name" : "get_current_city",
      "description":"Return the current city",
      "parameters" : {"type" : "object","properties" : {}}
    }
  },

  {
    "type" : "function",
    "function" : {
      "name" : "get_current_time",
      "description" : "Fetches the current timestamp to provide real-time temporal context for AI agent operations.",
      "parameters" : {"type" : "object" , "properties" : {}}
    }
  },
  {
    "type":"function",
    "function":{
      "name":"get_current_date",
      "description":"Returns the latest data available for the current day, enabling the AI agent to perform real-time analysis, decision-making, and task execution based on today's information.",
      "parameters":{"type":"object","properties":{}}
    }
  },
  {
    "type":"function",
    "function":{
      "name":"get_city_weather",
      "description":"Returns the current weather conditions for a specified city, enabling the AI agent to perform weather-aware analysis, recommendations, and actions.",
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
  "get_city_weather":get_city_weather,
  "get_current_city" : get_current_city
}
