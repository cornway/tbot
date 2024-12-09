import ollama
desiredModel='llama3.2:1b'

def chat_get_message(request):
    response = ollama.chat(model=desiredModel, messages=[
    {
        'role': 'user',
        'content': request,
    },
    ])

    OllamaResponse=response['message']['content']

    return OllamaResponse