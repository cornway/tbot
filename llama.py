import ollama
desiredModel='llama3.2:3b'
questionToAsk='Please translate the following text to polish : \"Скажите пожалуйста, сколько это стоит ?\"'

response = ollama.chat(model=desiredModel, messages=[
  {
    'role': 'user',
    'content': questionToAsk,
  },
])

OllamaResponse=response['message']['content']

print(OllamaResponse)

with open("OutputOllama.txt", "w", encoding="utf-8") as text_file:
    text_file.write(OllamaResponse)