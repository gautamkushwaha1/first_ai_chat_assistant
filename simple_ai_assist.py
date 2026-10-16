from openai import OpenAI
client = OpenAI(
  base_url="http://127.0.0.1:11434/v1",
  api_key="ollama"
)

response = client.chat.completions.create(
  model="qwen:latest",
  messages=[
    {
      "role":"user",
      "content":"hey,what's up !"
    }
  ]

)

print(response)