pip install flask flask_sqlalchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
db = SQLAlchemy(app)

# MODELOS
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    cpf = db.Column(db.String(11), unique=True)
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(100))

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especialidade = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'))
    data = db.Column(db.String(10))
    horario = db.Column(db.String(5))
    sintomas = db.Column(db.Text)

class Atestado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_nome = db.Column(db.String(100))
    medico_nome = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

# ROTAS
@app.route('/paciente', methods=['POST'])
def criar_paciente():
    data = request.json
    paciente = Paciente(**data)
    db.session.add(paciente)
    db.session.commit()
    return jsonify({'msg': 'Paciente cadastrado com sucesso'})

@app.route('/medico', methods=['POST'])
def criar_medico():
    data = request.json
    medico = Medico(**data)
    db.session.add(medico)
    db.session.commit()
    return jsonify({'msg': 'Médico cadastrado com sucesso'})

@app.route('/agendar', methods=['POST'])
def agendar_consulta():
    data = request.json
    agendamento = Agendamento(**data)
    db.session.add(agendamento)
    db.session.commit()
    return jsonify({'msg': 'Agendamento realizado'})

@app.route('/atestado', methods=['POST'])
def emitir_atestado():
    data = request.json
    atestado = Atestado(**data)
    db.session.add(atestado)
    db.session.commit()
    return jsonify({
        'paciente': atestado.paciente_nome,
        'medico': atestado.medico_nome,
        'tipo': atestado.tipo,
        'data_hora': atestado.data_hora.isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
