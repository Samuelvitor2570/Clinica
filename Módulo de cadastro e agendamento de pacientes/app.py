from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Armazenamento em memória
pacientes = []
agendamentos = []
usuarios = []

# Médicos disponíveis
MEDICOS = ['Dra. Ana Silva', 'Dra. Beatriz Lima', 'Dr. Carlos Mendes']

# Horários permitidos
HORARIOS_PERMITIDOS = ['08:00', '09:00', '10:00', '13:00', '14:00', '16:00']

# Filtro para formatar data
@app.template_filter('datetimeformat')
def datetimeformat(value):
    """Formata a data de YYYY-MM-DD para DD/MM/YYYY."""
    try:
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except ValueError:
        return value

# Funções auxiliares
def validar_telefone(telefone):
    """Valida se o telefone tem pelo menos 9 dígitos e contém apenas números."""
    return len(telefone) >= 9 and telefone.isdigit()

def validar_email(email):
    """Valida se o email contém um formato válido com @."""
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

def validar_cpf(cpf):
    """Valida se o CPF tem 11 dígitos e contém apenas números."""
    return len(cpf) == 11 and cpf.isdigit()

def validar_senha(senha):
    """Valida se a senha tem pelo menos 6 caracteres."""
    return len(senha) >= 6

def eh_dia_util(data_str):
    """Verifica se a data é de segunda a sexta-feira."""
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.weekday() < 5
    except ValueError:
        return False

def eh_horario_valido(horario_str):
    """Verifica se o horário está na lista de horários permitidos."""
    return horario_str in HORARIOS_PERMITIDOS

def contar_agendamentos(medico, data):
    """Conta o número de agendamentos para um médico em uma data específica."""
    return sum(1 for appt in agendamentos if appt['medico'] == medico and appt['data'] == data)

def horario_ocupado(medico, data, horario):
    """Verifica se o horário está ocupado para o médico na data especificada."""
    return any(appt['medico'] == medico and appt['data'] == data and appt['horario'] == horario for appt in agendamentos)

def paciente_cadastrado(email):
    """Verifica se o paciente está cadastrado pelo email."""
    return any(paciente['email'] == email for paciente in pacientes)

def usuario_cadastrado(email, senha):
    """Verifica se as credenciais do usuário são válidas."""
    return any(usuario['email'] == email and usuario['senha'] == senha for usuario in usuarios)

@app.route('/')
def index():
    """Rota padrão que redireciona para a página de login."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not all(key in request.form for key in ['email', 'senha']):
            flash('Formulário incompleto. Preencha todos os campos.', 'error')
            return render_template('login.html')
        
        email = request.form['email'].strip()
        senha = request.form['senha'].strip()
        
        erros = []
        if not email:
            erros.append('Email é obrigatório.')
        elif not validar_email(email):
            erros.append('Email inválido (deve conter @).')
        if not senha:
            erros.append('Senha é obrigatória.')
        
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('login.html')
        
        if usuario_cadastrado(email, senha):
            paciente = next((p for p in pacientes if p['email'] == email), None)
            if paciente:
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('agendamento', email=email, nome=paciente['nome'], telefone=paciente['telefone']))
            else:
                flash('Paciente não encontrado. Por favor, cadastre-se.', 'error')
                return redirect(url_for('cadastro'))
        else:
            flash('Credenciais inválidas. Verifique email e senha.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if not all(key in request.form for key in ['nome', 'email', 'telefone', 'cpf', 'senha']):
            flash('Formulário incompleto. Preencha todos os campos.', 'error')
            return render_template('cadastro.html')
        
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        telefone = request.form['telefone'].strip()
        cpf = request.form['cpf'].strip()
        senha = request.form['senha'].strip()
        
        erros = []
        if not nome:
            erros.append('Nome é obrigatório.')
        if not email:
            erros.append('Email é obrigatório.')
        elif not validar_email(email):
            erros.append('Email inválido (deve conter @).')
        if not telefone:
            erros.append('Telefone é obrigatório.')
        elif not validar_telefone(telefone):
            erros.append('Telefone deve ser numérico e ter 9 dígitos.')
        if not cpf:
            erros.append('CPF é obrigatório.')
        elif not validar_cpf(cpf):
            erros.append('CPF deve ser numérico e ter 11 dígitos.')
        if not senha:
            erros.append('Senha é obrigatória.')
        elif not validar_senha(senha):
            erros.append('Senha deve ter pelo menos 6 caracteres.')
        if any(u['email'] == email for u in usuarios):
            erros.append('Email já cadastrado.')
            
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('cadastro.html')
            
        paciente = {'nome': nome, 'email': email, 'telefone': telefone, 'cpf': cpf}
        usuarios.append({'email': email, 'senha': senha})
        pacientes.append(paciente)
        flash('Cadastro realizado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    email = request.args.get('email')
    nome = request.args.get('nome')
    telefone = request.args.get('telefone')
    
    if not email or not paciente_cadastrado(email):
        flash('Você precisa se logar antes de agendar.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if not all(key in request.form for key in ['nome', 'email', 'telefone', 'medico', 'data', 'horario', 'sintomas']):
            flash('Formulário de agendamento incompleto. Preencha todos os campos.', 'error')
            return render_template('agendamento.html', medicos=MEDICOS, email=email, nome=nome, telefone=telefone, horarios=HORARIOS_PERMITIDOS)
        
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        telefone = request.form['telefone'].strip()
        medico = request.form['medico'].strip()
        data = request.form['data'].strip()
        horario = request.form['horario'].strip()
        sintomas = request.form['sintomas'].strip()
        
        erros = []
        if not medico:
            erros.append('Médico é obrigatório.')
        if not horario:
            erros.append('Horário é obrigatório.')
        elif not eh_horario_valido(horario):
            erros.append('Horário inválido. Escolha um horário da lista.')
        if not data:
            erros.append('Data é obrigatória.')
        elif not eh_dia_util(data):
            erros.append('Consultas só podem ser marcadas de segunda a sexta.')
        if not sintomas:
            erros.append('Sintomas são obrigatórios.')
        if medico and data and contar_agendamentos(medico, data) >= 6:
            erros.append(f'O médico {medico} já tem o limite de 6 consultas no dia {data}.')
        if medico and data and horario and horario_ocupado(medico, data, horario):
            erros.append(f'O horário {horario} já está ocupado para o médico {medico} no dia {data}.')
            
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('agendamento.html', medicos=MEDICOS, email=email, nome=nome, telefone=telefone, horarios=HORARIOS_PERMITIDOS)
            
        agendamento = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'medico': medico,
            'data': data,
            'horario': horario,
            'sintomas': sintomas
        }
        agendamentos.append(agendamento)
        flash('Agendamento realizado com sucesso!', 'success')
        return render_template('agendamento.html', medicos=MEDICOS, email=email, nome=nome, telefone=telefone, horarios=HORARIOS_PERMITIDOS)
    
    return render_template('agendamento.html', medicos=MEDICOS, email=email, nome=nome, telefone=telefone, horarios=HORARIOS_PERMITIDOS)

@app.route('/agendamentos_cadastrados', methods=['GET'])
def agendamentos_cadastrados():
    medico_selecionado = request.args.get('medico', '')
    agendamentos_filtrados = [appt for appt in agendamentos if appt['medico'] == medico_selecionado] if medico_selecionado else []
    return render_template('agendamentos_cadastrados.html', medicos=MEDICOS, agendamentos=agendamentos_filtrados, medico_selecionado=medico_selecionado)

if __name__ == '__main__':
    app.run(debug=True)