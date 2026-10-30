#standard libarary imports
import os
from types import SimpleNamespace

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

def build_tool_call_payload(tool_calls):
  """convert all collect tool_calls into dict form
  that api expect in the assistant message"""

  payload = []
  for tool_call in tool_calls:
    pay_call_dict = {
      "id" : tool_call.id,
      "type" : "function",
      "function":{
        "name":tool_call.function.name,
        "arguments":tool_call.function.arguments,
      },
    }
    payload.append(pay_call_dict)

  return payload

def stream_chat(history):
  stream =client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages= history,
    tools=Tools,
    stream=True
  )

  full_response = ""
  calls = {}
  label_printed = False
  try:
    for chunk in stream:
      if not chunk.choices:
        continue

      delta = chunk.choices[0].delta

      # Content streaming

      if delta.content:
        if not label_printed:
          print("Assistant : " , end="", flush=True)
          label_printed = True
        print(delta.content,end="",flush=True)
        full_response += delta.content

      # Tools streaming

      for tc in (delta.tool_calls or []):
          obj = calls.setdefault(
            tc.index,
            SimpleNamespace(id = None , function = SimpleNamespace(name = "", arguments = "")),
          )
      
          if tc.id:
            obj.id = tc.id
      
          if tc.funtion and tc.function.name:
            obj.function.name += tc.function.name
      
          if tc.function and tc.function.argumnets:
            obj.function.arguments += tc.function.arguments

  except KeyboardInterrupt :
    print("\n{stopped by user}")
    calls = {}

  if label_printed:
    print() # move to the next line after assistant response.

  call_list = []

  for key in sorted(calls):
    call_list.append(calls[key])

  return full_response , call_list

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
  
  #chained tool_calling start
  for steps in range(max_step) :
    full_response , tool_calls = stream_chat(messages)
    
    # msg = response.choices[0].message

    if not tool_calls:
      break

    log(f"Steps {steps + 1} : Model Requested {len(tool_calls)}")

    messages.append({
      "role":"assistant",
      "content":full_response,
      "tool_calls":build_tool_call_payload(tool_calls)

    })
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
    

