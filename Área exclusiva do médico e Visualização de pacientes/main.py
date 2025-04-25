from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'secreto123'  # necessário para sessões

# Simulação de banco de dados
medicos = {
    1: {'nome': 'Dr. João'},
    2: {'nome': 'Dra. Maria'}
}

pacientes = [
    {'id': 1, 'nome': 'Carlos Silva', 'medico_id': 1},
    {'id': 2, 'nome': 'Ana Costa', 'medico_id': 1},
    {'id': 3, 'nome': 'José Santos', 'medico_id': 2},
]

@app.before_request
def simular_login():
    session['medico_id'] = 1  # médico logado é o de ID 1

@app.route('/medico/pacientes')
def listar_pacientes():
    medico_id = session.get('medico_id')
    termo_busca = request.args.get('busca', '').lower()
    
    pacientes_filtrados = [
        p for p in pacientes
        if p['medico_id'] == medico_id and termo_busca in p['nome'].lower()
    ]

    return render_template('pacientes.html', pacientes=pacientes_filtrados, busca=termo_busca)

@app.route('/prontuario/<int:paciente_id>')
def prontuario(paciente_id):
    return f"Prontuário do paciente {paciente_id}"
