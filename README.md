# Agent Test Demo Projects

Welcome to the demo-test repository for various LLM tools and experiments.

## Project Structure

Each project lives in its own folder and includes:

- `README.md` — Project-specific instructions
- `requirements.txt` — Python dependencies

Most projects use **Python** and **Flask APIs**. Some may include ESP32 scripts or other hardware-focused code.

## Getting Started

1. **Create a virtual environment (Python 3.11+ recommended):**

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment:**

    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

3. **Install dependencies for your chosen project:**

    ```bash
    pip install -r path/to/project/requirements.txt
    ```

4. **Read the project's `README.md` for specific instructions.**

---

## Frontend UI (`front-end-app/learning-front-end`)

A simple Svelte-based UI acts as an API wrapper for the Flask `/research` endpoint, providing a prompt-response interface.

### Installation & Running

1. **Install dependencies:**

    ```bash
    cd front-end-app/learning-front-end
    npm install
    ```

2. **Start the frontend server:**

    ```bash
    npm run dev
    ```

    The app will be available at [http://localhost:5173](http://localhost:5173) by default.

### Requirements

To use the frontend UI, ensure the following are running:

- **Ollama server** (for LLM backend)
- **Flask API** (`ollama_server_test/app.py`)
- **Frontend server** (see above)

CORS is currently allowed for development.

---

## Notes

- Each project is self-contained. You do you—follow the instructions, or blaze your own trail.
- Contributions, suggestions, and constructive sass are