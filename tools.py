from datetime import datetime

def get_current_time():
  return datetime.now()

Tools = [
  {
    "type" : "function",
    "function" : {
      "name" : "get_current_time",
      "description" : "Returns the current time and as formated string",
      "parameters" : {"t{ype" : "object" , "properties" : {}}
    }
    
  }
]

fuction_name_to_function_map = {
  "get_current_time" : get_current_time
}
