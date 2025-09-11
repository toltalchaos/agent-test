from flask import Flask, request, jsonify
import ollama
from ollama_server_test import settings
from ollama_server_test.custom_errors import NoModelResponse
from ollama_server_test.research.llm_actions import call_model
from ollama_server_test.research.prompt_improvement import improve_prompt
from ollama_server_test.research.reasearch import OllamaAuditor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/research', methods=['POST'])
def generate():
    """
    endpoint to generate a response from the model based on a given prompt.
    This endpoint also improves the prompt and audits the response for inaccuracies.
    Expects a JSON payload with a 'prompt' field.

    Example curl command:
    http://127.0.0.1:5000/research
    curl -X POST http://127.0.0.1:5000/research -H "Content-Type: application/json" -d '{"prompt": "What is the capital of France?"}'
    
    """
    try:
        prompt = request.json.get('prompt', '')
        original_prompt = prompt
        response = call_model(improve_prompt(prompt))
        auditor = OllamaAuditor(initial_prompt=prompt) # prompt here is redundant but for future use
        audited_response = auditor.audit_inaccuracy(original_prompt, response)
        return jsonify(audited_response), 200
    except NoModelResponse as e:
        return {'error': 'No response from model', 'message': str(e)}, 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    try:
        ollama.Client().health()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
    ollama.bye(settings.MODEL_NAME)