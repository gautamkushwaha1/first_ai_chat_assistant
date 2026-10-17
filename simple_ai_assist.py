from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv() #it looks for .env file and check for all envirnoment variable
client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY")
)

while True:
  user_input = input("Gautam : ")
  if user_input.lower() in ["exit", "bye","quit"]:
    break
  response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
      {
        "role":"user",
        "content":user_input
      }
    ]

  )
  
  print("Assistant : " + response.choices[0].message.content)

