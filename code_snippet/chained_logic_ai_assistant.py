#standard libarary imports
import os

#third_party library imports
from openai import OpenAI
from dotenv import load_dotenv

#Local modules
from tools import Tools , run_tools
from utilities.utilities import log


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

    log(f"Steps {steps + 1} : Model Requested {len(msg.tool_calls)}")

    messages.append(msg)
    for tool_call in msg.tool_calls:
      result = run_tools(tool_call)       
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
  
  
  print("Assistant : " + (msg.content or ""))