import pytest
from ..llm_actions import call_model
from ...custom_errors import NoModelResponse

def test_call_model_success(monkeypatch):
    class DummyClient:
        def generate(self, **kwargs):
            return {"response": "Because of Rayleigh scattering."}
    monkeypatch.setattr("ollama_server_test.research.llm_actions.Client", lambda host: DummyClient())
    result = call_model("why is the sky blue?")
    assert result == "Because of Rayleigh scattering."

def test_call_model_no_response(monkeypatch):
    class DummyClient:
        def generate(self, **kwargs):
            return None
    monkeypatch.setattr("ollama_server_test.research.llm_actions.Client", lambda host: DummyClient())
    with pytest.raises(NoModelResponse):
        call_model("why is the sky blue?")

def test_actual_model_response():
    # This test requires the actual model to be running and accessible.
    # It should be run in an environment where the model is available.
    try:
        response = call_model("What is the capital of France?")
        assert response is not None
    except NoModelResponse:
        pytest.skip("Model is not available for testing.")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")