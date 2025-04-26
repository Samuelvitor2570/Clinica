
!pip install flask


import os

os.makedirs("templates", exist_ok=True)

# main.py
with open("main.py", "w") as f:
    f.write('''
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
''')

# pacientes.html
with open("templates/pacientes.html", "w") as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Pacientes do Médico</title>
</head>
<body>
    <h1>Pacientes</h1>
    <form method="get">
        <input type="text" name="busca" placeholder="Buscar por nome" value="{{ busca }}">
        <button type="submit">Buscar</button>
    </form>
    <ul>
        {% for paciente in pacientes %}
        <li>
            {{ paciente.nome }} -
            <a href="{{ url_for('prontuario', paciente_id=paciente.id) }}">Ver prontuário</a>
        </li>
        {% else %}
        <li>Nenhum paciente encontrado.</li>
        {% endfor %}
    </ul>
</body>
</html>
''')

# 3. Rodar os testes
import unittest
import sys
import types

spec = types.ModuleType("main")
exec(open("main.py").read(), spec.__dict__)
app = spec.app

class MedicoPacientesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_listar_pacientes(self):
        response = self.app.get('/medico/pacientes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Carlos Silva', response.data)
        self.assertIn(b'Ana Costa', response.data)
        self.assertNotIn(b'Jos\xc3\xa9 Santos', response.data)

    def test_busca_paciente(self):
        response = self.app.get('/medico/pacientes?busca=ana')
        self.assertIn(b'Ana Costa', response.data)
        self.assertNotIn(b'Carlos Silva', response.data)

unittest.main(argv=[''], exit=False)
