# Ollama Quickstart Cheat Sheet

[Ollama Documentation](https://github.com/ollama/ollama/tree/main?tab=readme-ov-file)

A basic cheat sheet to get a model running with Ollama.

---

## 1. Create a Model

```sh
ollama create spymodel -f ./Modelfile
```

## 2. Run the Model

```sh
ollama run spymodel
```

- Type in the console to interact with the LLM.
- To exit, type:
    ```
    /bye
    ```

## 3. Stop the Model

```sh
ollama stop spymodel
```
