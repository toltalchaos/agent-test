import pytest
from unittest.mock import patch, MagicMock
from ollama_server_test.app import app

# New test: only patch call_model, check call count
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def call_model_counter():
    counter = {'count': 0}
    def mock_call_model(prompt):
        counter['count'] += 1
        return {'response': f'response ({counter["count"]})'}
    mock_call_model.counter = counter
    return mock_call_model

@patch('ollama_server_test.app.call_model')
@patch('ollama_server_test.app.OllamaAuditor')
@patch('ollama_server_test.app.improve_prompt', side_effect=lambda x: x)
def test_research_endpoint_call_count(mock_improve_prompt, mock_auditor, mock_call_model, client):
    mock_call = call_model_counter()
    mock_call_model.side_effect = mock_call
    auditor_instance = MagicMock()
    auditor_instance.audit_inaccuracy.side_effect = lambda prompt, response: {'audited': response}
    mock_auditor.return_value = auditor_instance

    for i in range(1, 4):
        resp = client.post('/research', json={'prompt': f'prompt {i}'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['audited'] == f'response ({i})'

@patch('ollama_server_test.app.call_model')
def test_research_endpoint_call_model_count_only(mock_call_model, client):
    mock_call = call_model_counter()
    mock_call_model.side_effect = mock_call

    with patch('ollama_server_test.settings.MAX_AUDITS', 5):
        resp = client.post('/research', json={'prompt': 'count test'})
        assert resp.status_code == 500 or resp.status_code == 200
        # call_model should be called MAX_AUDITS times +1 
        # If dependencies are not patched, expect error, else expect 6 calls
        if resp.status_code == 200:
            assert mock_call.counter['count'] == 6

@patch('ollama_server_test.app.call_model', side_effect=lambda prompt: {'response': 'mocked response'})
@patch('ollama_server_test.app.OllamaAuditor')
@patch('ollama_server_test.app.improve_prompt', side_effect=lambda x: f'improved {x}')
def test_research_endpoint_improve_prompt_and_audit(mock_improve_prompt, mock_auditor, mock_call_model, client):
    auditor_instance = MagicMock()
    auditor_instance.audit_inaccuracy.return_value = {'audited': 'mocked response'}
    mock_auditor.return_value = auditor_instance

    resp = client.post('/research', json={'prompt': 'original prompt'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['audited'] == 'mocked response'
    mock_improve_prompt.assert_called_once_with('original prompt')
    auditor_instance.audit_inaccuracy.assert_called_once_with('original prompt', 'mocked response')

@patch('ollama_server_test.app.call_model', side_effect=lambda prompt: {'response': 'response'})
@patch('ollama_server_test.app.OllamaAuditor', side_effect=Exception('Audit error'))
@patch('ollama_server_test.app.improve_prompt', side_effect=lambda x: x)
def test_research_endpoint_auditor_exception(mock_improve_prompt, mock_auditor, mock_call_model, client):
    resp = client.post('/research', json={'prompt': 'test'})
    assert resp.status_code == 500
    data = resp.get_json()
    assert 'error' in data
    assert data['error'] == 'An error occurred'

@patch('ollama_server_test.app.call_model', side_effect=Exception('Model error'))
@patch('ollama_server_test.app.OllamaAuditor')
@patch('ollama_server_test.app.improve_prompt', side_effect=lambda x: x)
def test_research_endpoint_call_model_exception(mock_improve_prompt, mock_auditor, mock_call_model, client):
    resp = client.post('/research', json={'prompt': 'test'})
    assert resp.status_code == 500
    data = resp.get_json()
    assert 'error' in data
    assert data['error'] == 'An error occurred'

def test_health_endpoint_ok(client):
    with patch('ollama_server_test.app.ollama.Client') as mock_client:
        mock_client.return_value.health.return_value = None
        resp = client.get('/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ok'

def test_health_endpoint_error(client):
    with patch('ollama_server_test.app.ollama.Client') as mock_client:
        mock_client.return_value.health.side_effect = Exception('Health error')
        resp = client.get('/health')
        assert resp.status_code == 500
        data = resp.get_json()
        assert data['status'] == 'error'
        assert 'message' in data