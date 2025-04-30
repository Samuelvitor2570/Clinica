import pytest
from app import app, validar_email, validar_telefone, eh_dia_util, eh_horario_valido, paciente_cadastrado, pacientes, agendamentos

@pytest.fixture
def client():
    """Configura o cliente de teste Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Limpa listas antes de cada teste
        pacientes.clear()
        agendamentos.clear()
        yield client
    # Limpa listas após cada teste
    pacientes.clear()
    agendamentos.clear()

def test_validar_telefone_valido(client):
    """Testa validação de telefone válido."""
    assert validar_telefone('123456789') is True

def test_validar_telefone_invalido(client):
    """Testa validação de telefone inválido."""
    assert validar_telefone('abc') is False
    assert validar_telefone('12345') is False  # Menos de 9 dígitos

def test_validar_email_valido(client):
    """Testa validação de email válido."""
    assert validar_email('teste@exemplo.com') is True

def test_validar_email_invalido(client):
    """Testa validação de email inválido."""
    assert validar_email('email_invalido') is False
    assert validar_email('teste@exemplo') is False  # Sem domínio completo

def test_eh_dia_util_segunda(client):
    """Testa se segunda-feira é dia útil."""
    assert eh_dia_util('2025-04-28') is True  # Segunda-feira

def test_eh_dia_util_domingo(client):
    """Testa se domingo não é dia útil."""
    assert eh_dia_util('2025-04-27') is False  # Domingo

def test_eh_horario_valido_ok(client):
    """Testa validação de horário permitido."""
    assert eh_horario_valido('08:00') is True

def test_eh_horario_valido_invalido(client):
    """Testa validação de horário não permitido."""
    assert eh_horario_valido('11:00') is False

def test_paciente_cadastrado_true(client):
    """Testa verificação de paciente cadastrado."""
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789'})
    assert paciente_cadastrado('teste@exemplo.com') is True

def test_paciente_cadastrado_false(client):
    """Testa verificação de paciente não cadastrado."""
    assert paciente_cadastrado('nao_existe@exemplo.com') is False

def test_cadastro_faltando_nome(client):
    """Testa cadastro com nome ausente."""
    response = client.post('/cadastro', data={
        'nome': '',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Nome é obrigatório.' in response.data.decode('utf-8')

def test_cadastro_faltando_email(client):
    """Testa cadastro com email ausente."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': '',
        'telefone': '123456789'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email é obrigatório.' in response.data.decode('utf-8')

def test_cadastro_email_invalido(client):
    """Testa cadastro com email sem formato válido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'email_invalido',
        'telefone': '123456789'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email inválido (deve conter @).' in response.data.decode('utf-8')

def test_cadastro_faltando_telefone(client):
    """Testa cadastro com telefone ausente."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': ''
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Telefone é obrigatório.' in response.data.decode('utf-8')

def test_cadastro_telefone_curto(client):
    """Testa cadastro com telefone inválido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': 'abc'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Telefone deve ser numérico e ter 9 dígitos.' in response.data.decode('utf-8')

def test_agendamento_faltando_medico(client):
    """Testa agendamento com médico ausente."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': '',
        'data': '2025-04-28',
        'horario': '10:00'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Médico é obrigatório.' in response.data.decode('utf-8')

def test_agendamento_faltando_horario(client):
    """Testa agendamento com horário ausente."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': ''
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Horário é obrigatório.' in response.data.decode('utf-8')

def test_limite_agendamentos(client):
    """Testa o limite de 6 agendamentos por médico por dia."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    horarios = ['08:00', '09:00', '10:00', '13:00', '14:00', '16:00']
    for i in range(6):
        agendamentos.append({
            'nome': f'Teste{i}',
            'email': 'teste@exemplo.com',
            'telefone': '123456789',
            'medico': 'Dra. Ana Silva',
            'data': '2025-04-28',
            'horario': horarios[i]
        })
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '08:00'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'O médico Dra. Ana Silva já tem o limite de 6 consultas no dia 2025-04-28.' in response.data.decode('utf-8')

def test_cadastro_valido(client):
    """Testa um cadastro válido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert 'email=teste@exemplo.com&nome=Teste&telefone=123456789' in response.location
    assert len(pacientes) == 1
    assert pacientes[0]['nome'] == 'Teste'

def test_agendamento_valido(client):
    """Testa um agendamento válido após cadastro."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Agendamento realizado com sucesso!' in response.data.decode('utf-8')
    assert len(agendamentos) == 1
    assert agendamentos[0]['medico'] == 'Dra. Ana Silva'
    # Verifica se nome e telefone são readonly
    response = client.get('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789')
    assert 'name="nome" value="Teste"' in response.data.decode('utf-8')
    assert 'readonly' in response.data.decode('utf-8')
    assert 'name="telefone" value="123456789"' in response.data.decode('utf-8')

def test_agendamento_mesmo_horario(client):
    """Testa tentativa de agendar no mesmo horário para o mesmo médico e data."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    # Primeiro agendamento
    client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00'
    }, follow_redirects=False)
    # Tentativa de agendar no mesmo horário
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste2',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'O horário 10:00 já está ocupado para o médico Dra. Ana Silva no dia 2025-04-28.' in response.data.decode('utf-8')

def test_agendamentos_cadastrados(client):
    """Testa a página de agendamentos cadastrados com filtro por médico."""
    client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789'
    }, follow_redirects=False)
    client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00'
    }, follow_redirects=False)
    # Acessa a página sem filtro
    response = client.get('/agendamentos_cadastrados')
    assert response.status_code == 200
    assert 'Selecione um médico para ver os agendamentos.' in response.data.decode('utf-8')
    # Acessa a página com filtro
    response = client.get('/agendamentos_cadastrados?medico=Dra. Ana Silva')
    assert response.status_code == 200
    assert 'Agendamentos de Dra. Ana Silva' in response.data.decode('utf-8')
    assert 'Teste' in response.data.decode('utf-8')
    assert 'teste@exemplo.com' in response.data.decode('utf-8')
    assert '123456789' in response.data.decode('utf-8')
    assert '2025-04-28' in response.data.decode('utf-8')
    assert '10:00' in response.data.decode('utf-8')
