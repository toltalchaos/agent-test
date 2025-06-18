
from ollama_server_test.research.llm_actions import call_model


def improve_prompt(prompt: str) -> str:
    """
    Takes a prompt string, asks an LLM to improve it, and returns the improved prompt.
    """
    system_message = (
        "You are an expert prompt engineer. Given a prompt, improve it so that it will yield better, more accurate, and more detailed results from a large language model. "
        "Return only the improved prompt."
    )
    response = call_model(prompt, system_message=system_message) 
    improved_prompt = response.choices[0].message['content'].strip() #need to debug here to see if this is correct
    return improved_prompt