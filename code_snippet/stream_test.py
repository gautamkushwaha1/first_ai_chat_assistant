import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY")
)

stream = client.chat.completions.create(
  model=os.getenv("MODEL"),
  messages=[{"role":"user","content":"explain me the python language in 100 words"}],
  stream= True

)

for chunk in stream:
  if not chunk.choices:
    continue
  
  piece = chunk.choices[0].delta
  if piece.content:
    print(piece.content , end="", flush=True)