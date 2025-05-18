import pytest
from app import app  # Importe a aplicação do arquivo app.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_selecionar_medico(client):
    response = client.get('/?medico=Dra. Beatriz Lima')
    assert 'Pacientes de Dra. Beatriz Lima' in response.get_data(as_text=True)

def test_exibir_pacientes(client):
    response = client.get('/?medico=Dra. Beatriz Lima')
    assert 'Marcos Almeida' in response.get_data(as_text=True)

def test_buscar_paciente(client):
    response = client.post('/', data={'nome': 'Laura Souza'})
    assert 'Laura Souza' in response.get_data(as_text=True)

def test_nenhum_paciente_encontrado(client):
    response = client.post('/', data={'nome': 'João Silva'})
    assert 'Nenhum paciente encontrado.' in response.get_data(as_text=True)
