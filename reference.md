### llm_flask_rag_agent/app.py

from flask import Flask, request, jsonify
from llm_wrapper import run_llm
from tools import tools
from retriever import retrieve_relevant, load_documents
import json

app = Flask(__name__)
load_documents()

@app.route("/query", methods=["POST"])
def query():
    user_prompt = request.json.get("prompt")

    # RAG: retrieve documents and inject into prompt
    context_docs = retrieve_relevant(user_prompt)
    context = "\n\n".join(context_docs)

    full_prompt = f"""You are a helpful assistant.

Context:
{context}

User question:
{user_prompt}

If the question requires a tool, respond with:
{{"function_call": {{"name": "function_name"}}}}

Otherwise, just answer normally."""

    response = run_llm(full_prompt)

    # Parse function call
    if '"function_call":' in response:
        try:
            call_data = json.loads(response)
            fn_name = call_data["function_call"]["name"]
            if fn_name in tools:
                fn_result = tools[fn_name]()
                final_prompt = f"You previously said to call `{fn_name}`, which returned this result:\n{fn_result}\n\nNow answer the original question: {user_prompt}"
                answer = run_llm(final_prompt)
                return jsonify({
                    "intermediate_function": fn_name,
                    "function_result": fn_result,
                    "final_answer": answer
                })
        except Exception as e:
            return jsonify({"error": "Failed to parse function call", "raw_response": response})

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)


### llm_flask_rag_agent/llm_wrapper.py

from llama_cpp import Llama

llm = Llama(
    model_path="./models/mistral-7b-instruct.gguf",
    n_ctx=2048,
    n_threads=8
)

def run_llm(prompt, max_tokens=512):
    output = llm(prompt, max_tokens=max_tokens, stop=["</s>"])
    return output["choices"][0]["text"].strip()


### llm_flask_rag_agent/tools.py

def get_weather():
    return {"temp": 22, "condition": "Cloudy"}

tools = {
    "get_weather": get_weather
}


### llm_flask_rag_agent/retriever.py

import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
docs = []
embeddings = []

def load_documents(path="data"):
    for file in Path(path).glob("*.txt"):
        text = file.read_text()
        docs.append(text)
        emb = model.encode([text])[0]
        embeddings.append(emb)

    index.add(np.array(embeddings).astype("float32"))

def retrieve_relevant(query, top_k=1):
    q_emb = model.encode([query])
    _, I = index.search(np.array(q_emb).astype("float32"), top_k)
    return [docs[i] for i in I[0]]


### llm_flask_rag_agent/requirements.txt

flask
llama-cpp-python
requests
faiss-cpu
sentence-transformers


### llm_flask_rag_agent/README.md

# LLM Flask Agent with RAG and Function Calling

This template provides a Flask API that:
- Hosts a **local LLM** (using `llama-cpp-python`)
- Supports **structured function calling**
- Uses **RAG** to retrieve and inject context into prompts

## 🛠 Setup

```bash
# Clone this repo
cd llm_flask_rag_agent
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🤖 Download a .gguf Model
Download a `.gguf` LLM (e.g. [Mistral](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)) into the `models/` directory.

```
mkdir -p models
download model to: models/mistral-7b-instruct.gguf
```

## 📂 Add RAG Documents
Put `.txt` files in the `data/` directory. These will be embedded and searched.

```
mkdir data
echo "Canada is a country in North America." > data/example.txt
```

## 🚀 Run the App

```bash
python app.py
```

POST requests to:
```http
POST http://localhost:5000/query
{
  "prompt": "What is the weather like?"
}
```

## 📦 Features
- 🔁 RAG: pulls relevant knowledge into the prompt
- 🔧 Structured tool calls: like `{"function_call": {"name": "get_weather"}}`
- 🧠 Fully local, no API key needed

---

You can extend it by adding more tools in `tools.py`, more documents to `data/`, and additional logic for reasoning loops.

PRs welcome!
