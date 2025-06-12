from flask import Flask, request, jsonify
from ollama_server_test.custom_errors import NoModelResponse
from ollama_server_test.research.llm_actions import call_model
from ollama_server_test.research.reasearch import OllamaAuditor

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json.get('prompt', '')
        response = call_model(prompt)
        auditor = OllamaAuditor(initial_prompt=prompt) # prompt here is redundant but for future use
        audited_response = auditor.audit_inaccuracy(prompt, response.get('response', ''))
        return jsonify(audited_response)
    except NoModelResponse as e:
        return jsonify({'error': 'No response from model', 'message': str(e)}), 500
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