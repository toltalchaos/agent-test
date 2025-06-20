from ollama import Client
from ollama_server_test.custom_errors import NoModelResponse
from ollama_server_test.settings import * # i know * isnt great practice. pretend its not there.
# https://github.com/ollama/ollama-python
def call_model(prompt, system_message=SYSTEM):
    '''this assumes the model is already running and available at MODEL_URL'''
    client = Client(host=MODEL_URL, temperature=TEMPERATURE, max_tokens= MAX_TOKENS, system=system_message)  # Initialize the Ollama client with the model server URL
    response = client.generate(model=MODEL_NAME, prompt=prompt,)
    if not response:
        raise NoModelResponse("No response from model")
    return response.get("response", "").strip()