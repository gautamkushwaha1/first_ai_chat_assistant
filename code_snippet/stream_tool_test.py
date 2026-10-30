import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import Tools
from types import SimpleNamespace

load_dotenv()
client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY")
)

stream = client.chat.completions.create(
  model=os.getenv("MODEL"),
  messages=[{"role":"user","content":"what is the weather condition of bihar  and delhi right now?"}],
  tools=Tools,
  stream=True
)


full_response = ""

calls = {}

for chunks in stream:
  if not chunks.choices:
    continue

  delta = chunks.choices[0].delta

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

call_list = []

for key in sorted(calls):
  call_list.append(calls[key])



# print(f"\n\nfull_response {full_response}")