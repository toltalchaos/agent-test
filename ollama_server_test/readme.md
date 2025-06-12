# Ollama Local LLM + Flask API Boilerplate

This guide helps you set up a local LLM using [Ollama](https://ollama.com/) and interact with the available http server with a client via a Flask API.

## Prerequisites

- [Ollama installed](https://ollama.com/download)
- Python 3.8+
- `pip` package manager

## 1. Start Ollama and Pull a Model

```sh
ollama serve
ollama pull llama2
```

## 2. Set Up Flask and Ollama Client

Install dependencies:

```sh
pip install flask ollama
```

## 3. Example Flask API

Create `app.py`:

```python
from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt', '')
    response = ollama.Client().generate(model='llama2', prompt=prompt)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

## 4. Run the Flask API

```sh
python app.py
```

## 5. Test the API

```sh
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Hello, world!"}'
```

---

**You now have a local LLM running with Ollama and a Flask API to interact with it!**