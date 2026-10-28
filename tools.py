from datetime import datetime , date
import requests
import json
from utilities.utilities import log

def get_current_time():
  return datetime.now().strftime(" %B %d , %Y at %I:%M %p")

def get_current_date():
  return date.today()

def get_city_weather(city):
  url = f"https://wttr.in/{city}?format=3"
  response = requests.get(url,timeout = 10)
  response.raise_for_status()
  return response.text

def get_current_city():
  return "delhi"

Tools = [

  {
    "type" : "function",
    "function" : {
      "name" : "get_current_city",
      "description":"Return the current city when words like 'my city' , 'my current city' presents ",
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
        },
        "required" : ["city"]

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

def run_tools(tool_call):
  func_name = tool_call.function.name
  try:
    func_args = json.loads(tool_call.function.arguments or "{}")
    log(f" {func_name} -> {func_args}")
    fn = fuction_name_to_function_map[func_name]
    result = fn(**func_args)
  except Exception as e:
    result = f"error while running {func_name} : {e}"

  log(f"  ---> {result}") 
  return str(result)
