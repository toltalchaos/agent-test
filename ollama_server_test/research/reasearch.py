from ollama_server_test.research.llm_actions import call_model
from ollama_server_test.settings import MAX_AUDITS

class OllamaAuditor:
    #later on i would like to add a report function that will return a report of the audits done just to terminal (or atleast not-to-user)
    def __init__(self, initial_prompt): #this might seem weird but il want a report on the audit after the fact later down the line
        self.number_of_audits = 0
        self.initial_prompt = initial_prompt
        # Initialize the prompt and response to a default state
        self.prompt = 'init state'
        self.response = 'init state'

    def audit_inaccuracy(self, prompt: str, response: str):
        """
        Loop to check for inaccuracies in the response using the Ollama client.
        Returns a corrected response if inaccuracies are found, otherwise returns the original response.
        :param prompt: The original prompt sent to the model.
        :param response: The response received from the model.
        :return: A corrected response if inaccuracies were found, otherwise the original response.
        """
        self.number_of_audits += 1
        inaccuracies = []
        self.prompt = prompt
        self.response = response
        for _ in range(MAX_AUDITS):
            audit_prompt = (
                f"Given the following prompt and response, identify any additional inaccuracies in the response.\n"
                f"Prompt: {self.prompt}\n"
                f"Response: {self.response}\n"
                f"inaccuracies: {', '.join(inaccuracies) if inaccuracies else 'None'}\n"
                f"List any inaccuracies or reply 'None' if there are none."
            )
            result = call_model(audit_prompt)
            answer = result.get("response", "").strip()
            if answer.lower() == "none":
                continue
            inaccuracies.append(answer)
        # If no inaccuracies were found, return None
        if inaccuracies == []:
            return None
        # If inaccuracies were found, generate a new response correcting them
        audited_prompt = (
            "respond to the following prompt without inaccuracies identified\n"
            f"Prompt: {self.prompt}\n"
            f"Identified inaccuracies: {', '.join(inaccuracies) if inaccuracies else 'None'}\n"
        )
        fixed_response = call_model(audited_prompt)
        return fixed_response if inaccuracies else response
        # Return the fixed response if inaccuracies were found, otherwise return the original response

# later on i would like to add some functionality to research the inaccuracies or atleast provide supporting citations for the response given (which is why audit looping is important)
    
