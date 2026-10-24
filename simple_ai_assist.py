from openai import OpenAI
from dotenv import load_dotenv
from tools import Tools , fuction_name_to_function_map
import json
import os
load_dotenv() #it looks for .env file and check for all envirnoment variable
client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY")
)
messages = []
messages.append(
  {
    "role":"system",
    "content":"act like a humble agent and respond always under 50 words"
  }
)

max_step = 10 # tool calling limit
while True:
  user_input = input("Gautam : ")
  if (user_input.lower()).strip() in ["exit", "bye","quit"]:
    break

  messages.append(
    {
      "role":"user",
      "content":user_input
    }
  )
  

  for steps in range(max_step) :
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools = Tools
      )
    
    msg = response.choices[0].message

    if not msg.tool_calls:
      break

    messages.append(msg)
    for tool_call in msg.tool_calls:
      func_name = tool_call.function.name
      try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        fn = fuction_name_to_function_map[func_name]
        result = fn(**func_args)
      except Exception as e:
        result = f"error while running {func_name} : {e}"


      messages.append(
        {
          "role":"tool",
          "tool_id":tool_call.id,
          "content":str(result)
        }
      )
  else:
    fallback = "sorry , we could not finish this within step limit"  
    messages.append({
      "role" : "assistant",
      "content":fallback
    }
      
    )
    print("assistant + ", fallback)
    continue
    

    

  messages.append(
    {
      "role":"assistant",
      "content":msg.content
    }
  )
  
  
  print("Assistant : " + msg.content)

