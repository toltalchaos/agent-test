# Ollama Local LLM + Flask API Boilerplate

This guide walks you through setting up a local Large Language Model (LLM) using [Ollama](https://ollama.com/) and exposing it via a RESTful API using Flask. By the end, you'll be able to interact with your LLM both from the command line and over HTTP.

---

## Prerequisites

- [Ollama installed](https://ollama.com/download)
- Python 3.8 or newer
- `pip` package manager

- may also be worth referencing [THIS](https://www.hongkiat.com/blog/ollama-llm-from-external-drive/) article if there are concerns about hard drive space

---

## 1. Start Ollama and Pull a Model

First, start the Ollama server and pull a base model (e.g., `llama3.2`):

```sh
ollama serve
ollama pull llama3.2
```

---

## 2. Install Python Dependencies

Install Flask and the Ollama Python client:

```sh
pip install flask ollama
```

---

## 3. Run a Local LLM Model

To run a custom or default model locally:

1. **Start the Ollama server** (if not already running):

    ```sh
    ollama serve
    ```

2. **Create and run a model** (example: `teacher`):

    ```sh
    ollama create teacher -f ./Modelfile
    ollama run teacher
    ```

    - The model will be available at `http://localhost:11434` (default Ollama endpoint).
    - You can interact with the model via the CLI or programmatically.

3. **Stop the model** when done:

    ```sh
    ollama stop teacher
    ```

    or, in the active terminal:
    ```sh
    /bye
    ```

---

## 4. Run the Flask API

Start the Flask API server to provide a REST interface to your local LLM:

```sh
python ollama_server_test/app.py
```

### 4.1 Expose the API to the Local Network

To make the API accessible from other devices on your network:

```sh
flask --app ollama_server_test/app run --host=0.0.0.0
```

---

## 5. Test the API

Send a POST request to the `/research` endpoint with a prompt:

```sh
curl -X POST http://localhost:5000/research \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Why is the sky blue"}'
```

---

## Additional Notes

- **Model Customization:** Edit `Modelfile` to define your own model parameters or prompts. (also will want to see the `settings.py` file)
- **API Endpoints:** The default endpoint is `/research`, but you can extend `app.py` to add more functionality.
- **Security:** For production use, secure your API and consider authentication.

---

**You now have a local LLM running with Ollama and a Flask API to interact with it programmatically!**