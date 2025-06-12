from ollama import Client
from ollama_server_test.custom_errors import NoModelResponse
from ollama_server_test.settings import * # i know * isnt great practice. pretend its not there.

def call_model(prompt):
    client = Client(host=MODEL_URL)  # Initialize the Ollama client with the model server URL
    response = client.generate(model=MODEL_NAME, prompt=prompt, temperature= TEMPERATURE, max_tokens= MAX_TOKENS)
    if not response:
        raise NoModelResponse("No response from model")
    return response.get("response", "").strip()