import ollama
from ollama_server_test.custom_errors import NoModelResponse
from ollama_server_test.settings import * # i know * isnt great practice. pretend its not there.
# https://github.com/ollama/ollama-python
def call_model(prompt, system_message=SYSTEM):
    '''this assumes the model is already running and available at MODEL_URL'''
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': prompt}
    ]
    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
    )
    if not response:
        raise NoModelResponse("No response from model")
    return response['message']['content'].strip()
