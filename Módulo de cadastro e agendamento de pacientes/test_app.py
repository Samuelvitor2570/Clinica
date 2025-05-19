import pytest
from app import app, validar_telefone, validar_email, validar_cpf, validar_senha, eh_dia_util, eh_horario_valido, paciente_cadastrado, usuario_cadastrado, pacientes, agendamentos, usuarios

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        pacientes.clear()
        agendamentos.clear()
        usuarios.clear()
        yield client
    pacientes.clear()
    agendamentos.clear()
    usuarios.clear()

def test_validar_telefone_valido(client):
    """Testa se um telefone com 9 dígitos é válido."""
    assert validar_telefone('123456789') is True

def test_validar_telefone_invalido(client):
    """Testa se um telefone com menos de 9 dígitos é inválido."""
    assert validar_telefone('12345678') is False

def test_validar_email_valido(client):
    """Testa se um email com formato válido é aceito."""
    assert validar_email('teste@exemplo.com') is True

def test_validar_email_invalido(client):
    """Testa se um email sem @ é rejeitado."""
    assert validar_email('teste.exemplo.com') is False

def test_validar_cpf_valido(client):
    """Testa se um CPF com 11 dígitos é válido."""
    assert validar_cpf('12345678901') is True

def test_validar_cpf_invalido(client):
    """Testa se um CPF com menos de 11 dígitos é inválido."""
    assert validar_cpf('1234567890') is False

def test_validar_senha_valida(client):
    """Testa se uma senha com 6 ou mais caracteres é válida."""
    assert validar_senha('123456') is True

def test_validar_senha_invalida(client):
    """Testa se uma senha com menos de 6 caracteres é inválida."""
    assert validar_senha('12345') is False

def test_eh_dia_util_segunda(client):
    """Testa se uma segunda-feira é considerada dia útil."""
    assert eh_dia_util('2025-04-28') is True

def test_eh_dia_util_domingo(client):
    """Testa se um domingo é considerado não útil."""
    assert eh_dia_util('2025-04-27') is False

def test_eh_horario_valido_ok(client):
    """Testa se um horário permitido é válido."""
    assert eh_horario_valido('08:00') is True

def test_eh_horario_valido_invalido(client):
    """Testa se um horário não permitido é inválido."""
    assert eh_horario_valido('12:00') is False

def test_paciente_cadastrado_true(client):
    """Testa se um paciente cadastrado é encontrado."""
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    assert paciente_cadastrado('teste@exemplo.com') is True

def test_paciente_cadastrado_false(client):
    """Testa se um paciente não cadastrado não é encontrado."""
    assert paciente_cadastrado('naoexiste@exemplo.com') is False

def test_usuario_cadastrado_true(client):
    """Testa se um usuário cadastrado é encontrado."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    assert usuario_cadastrado('teste@exemplo.com', '123456') is True

def test_usuario_cadastrado_false(client):
    """Testa se um usuário não cadastrado não é encontrado."""
    assert usuario_cadastrado('teste@exemplo.com', '123456') is False

def test_cadastro_faltando_nome(client):
    """Testa cadastro sem nome."""
    response = client.post('/cadastro', data={
        'nome': '',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Nome é obrigatório.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_faltando_email(client):
    """Testa cadastro sem email."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': '',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email é obrigatório.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_email_invalido(client):
    """Testa cadastro com email inválido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste.exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email inválido (deve conter @).' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_faltando_telefone(client):
    """Testa cadastro sem telefone."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Telefone é obrigatório.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_telefone_invalido(client):
    """Testa cadastro com telefone inválido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '12345678',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Telefone deve ser numérico e ter 9 dígitos.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_faltando_cpf(client):
    """Testa cadastro sem CPF."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'CPF é obrigatório.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_cpf_invalido(client):
    """Testa cadastro com CPF inválido."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '1234567890',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'CPF deve ser numérico e ter 11 dígitos.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_faltando_senha(client):
    """Testa cadastro sem senha."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': ''
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Senha é obrigatória.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_senha_curta(client):
    """Testa cadastro com senha curta."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '12345'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Senha deve ter pelo menos 6 caracteres.' in response.data.decode('utf-8')
    assert len(pacientes) == 0
    assert len(usuarios) == 0

def test_cadastro_email_ja_cadastrado(client):
    """Testa cadastro com email já cadastrado."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email já cadastrado.' in response.data.decode('utf-8')
    assert len(pacientes) == 0

def test_cadastro_valido(client):
    """Testa cadastro com dados válidos."""
    response = client.post('/cadastro', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'cpf': '12345678901',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert 'login' in response.location
    assert len(pacientes) == 1
    assert len(usuarios) == 1

def test_login_faltando_email(client):
    """Testa login sem email."""
    response = client.post('/login', data={
        'email': '',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email é obrigatório.' in response.data.decode('utf-8')

def test_login_email_invalido(client):
    """Testa login com email inválido."""
    response = client.post('/login', data={
        'email': 'teste.exemplo.com',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Email inválido (deve conter @).' in response.data.decode('utf-8')

def test_login_faltando_senha(client):
    """Testa login sem senha."""
    response = client.post('/login', data={
        'email': 'teste@exemplo.com',
        'senha': ''
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Senha é obrigatória.' in response.data.decode('utf-8')

def test_login_credenciais_invalidas(client):
    """Testa login com credenciais inválidas."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    response = client.post('/login', data={
        'email': 'teste@exemplo.com',
        'senha': '123457'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Credenciais inválidas. Verifique email e senha.' in response.data.decode('utf-8')

def test_login_paciente_nao_cadastrado(client):
    """Testa login com paciente não cadastrado."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    response = client.post('/login', data={
        'email': 'teste@exemplo.com',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert 'cadastro' in response.location

def test_login_valido(client):
    """Testa login com credenciais válidas."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    response = client.post('/login', data={
        'email': 'teste@exemplo.com',
        'senha': '123456'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert 'agendamento' in response.location

def test_agendamento_faltando_medico(client):
    """Testa agendamento sem médico."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': '',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': 'Febre e dor de cabeça'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Médico é obrigatório.' in response.data.decode('utf-8')
    assert len(agendamentos) == 0

def test_agendamento_faltando_horario(client):
    """Testa agendamento sem horário."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '',
        'sintomas': 'Febre e dor de cabeça'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Horário é obrigatório.' in response.data.decode('utf-8')
    assert len(agendamentos) == 0

def test_agendamento_faltando_sintomas(client):
    """Testa agendamento sem sintomas."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': ''
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Sintomas são obrigatórios.' in response.data.decode('utf-8')
    assert len(agendamentos) == 0

def test_limite_agendamentos(client):
    """Testa o limite de 6 agendamentos por médico por dia."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    horarios = ['08:00', '09:00', '10:00', '13:00', '14:00', '16:00']
    for i in range(6):
        agendamentos.append({
            'nome': f'Teste{i}',
            'email': 'teste@exemplo.com',
            'telefone': '123456789',
            'medico': 'Dra. Ana Silva',
            'data': '2025-04-28',
            'horario': horarios[i],
            'sintomas': 'Febre'
        })
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '16:00',
        'sintomas': 'Febre'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'O médico Dra. Ana Silva já tem o limite de 6 consultas no dia 2025-04-28.' in response.data.decode('utf-8')
    assert len(agendamentos) == 6

def test_agendamento_valido(client):
    """Testa agendamento com dados válidos."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': 'Febre e dor de cabeça'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'Agendamento realizado com sucesso!' in response.data.decode('utf-8')
    assert len(agendamentos) == 1

def test_agendamento_mesmo_horario(client):
    """Testa agendamento no mesmo horário de um existente."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    agendamentos.append({
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': 'Febre'
    })
    response = client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': 'Febre e dor de cabeça'
    }, follow_redirects=False)
    assert response.status_code == 200
    assert 'O horário 10:00 já está ocupado para o médico Dra. Ana Silva no dia 2025-04-28.' in response.data.decode('utf-8')
    assert len(agendamentos) == 1

def test_agendamentos_cadastrados(client):
    """Testa a página de agendamentos cadastrados com filtro por médico."""
    usuarios.append({'email': 'teste@exemplo.com', 'senha': '123456'})
    pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789', 'cpf': '12345678901'})
    client.post('/agendamento?email=teste@exemplo.com&nome=Teste&telefone=123456789', data={
        'nome': 'Teste',
        'email': 'teste@exemplo.com',
        'telefone': '123456789',
        'medico': 'Dra. Ana Silva',
        'data': '2025-04-28',
        'horario': '10:00',
        'sintomas': 'Febre e dor de cabeça'
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
    assert '28/04/2025' in response.data.decode('utf-8')
    assert '10:00' in response.data.decode('utf-8')
    assert 'Febre e dor de cabeça' in response.data.decode('utf-8')