from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Armazenamento em memória
pacientes = []
agendamentos = []

# Médicos disponíveis
MEDICOS = ['Dr. Ana Silva', 'Dr. Carlos Mendes', 'Dr. Beatriz Lima']

# Horários permitidos
HORARIOS_PERMITIDOS = ['08:00', '09:00', '10:00', '13:00', '14:00', '16:00']

# Funções auxiliares
def validar_telefone(telefone):
    """Valida se o telefone tem pelo menos 9 dígitos e contém apenas números."""
    return len(telefone) >= 9 and telefone.isdigit()

def validar_email(email):
    """Valida se o email contém um formato válido com @."""
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

def eh_dia_util(data_str):
    """Verifica se a data é de segunda a sexta-feira."""
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.weekday() < 5  # Segunda a sexta
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

@app.route('/')
def index():
    """Rota padrão que redireciona para a página de cadastro."""
    return redirect(url_for('cadastro'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Verifica se os campos existem no formulário
        if not all(key in request.form for key in ['nome', 'email', 'telefone']):
            flash('Formulário incompleto. Preencha todos os campos.', 'error')
            return render_template('cadastro.html')
        
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        
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
            erros.append('Telefone deve ter pelo menos 9 dígitos.')
            
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('cadastro.html')
            
        paciente = {'nome': nome, 'email': email, 'telefone': telefone}
        pacientes.append(paciente)
        flash('Cadastro realizado com sucesso! Agora você pode agendar sua consulta.', 'success')
        return redirect(url_for('agendamento', email=email))
    
    return render_template('cadastro.html')

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    email = request.args.get('email')
    if not email or not paciente_cadastrado(email):
        flash('Você precisa se cadastrar antes de agendar.', 'error')
        return redirect(url_for('cadastro'))
    
    if request.method == 'POST':
        # Verifica se os campos existem no formulário
        if not all(key in request.form for key in ['nome', 'email', 'telefone', 'medico', 'data', 'horario']):
            flash('Formulário de agendamento incompleto. Preencha todos os campos.', 'error')
            return render_template('agendamento.html', medicos=MEDICOS, agendamentos=agendamentos, email=email, horarios=HORARIOS_PERMITIDOS)
        
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        medico = request.form['medico']
        data = request.form['data']
        horario = request.form['horario']
        
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
        if medico and data and contar_agendamentos(medico, data) >= 6:
            erros.append(f'O médico {medico} já tem o limite de 6 consultas no dia {data}.')
        if medico and data and horario and horario_ocupado(medico, data, horario):
            erros.append(f'O horário {horario} já está ocupado para o médico {medico} no dia {data}.')
            
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return render_template('agendamento.html', medicos=MEDICOS, agendamentos=agendamentos, email=email, horarios=HORARIOS_PERMITIDOS)
            
        agendamento = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'medico': medico,
            'data': data,
            'horario': horario
        }
        agendamentos.append(agendamento)
        flash('Agendamento realizado com sucesso!', 'success')
        return render_template('agendamento.html', medicos=MEDICOS, agendamentos=agendamentos, email=email, horarios=HORARIOS_PERMITIDOS)
    
    return render_template('agendamento.html', medicos=MEDICOS, agendamentos=agendamentos, email=email, horarios=HORARIOS_PERMITIDOS)

if __name__ == '__main__':
    app.run(debug=True)