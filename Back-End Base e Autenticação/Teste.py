import unittest
import json
from app import app, db, Paciente, Medico, Agendamento, Atestado

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def test_criar_paciente(self):
        response = self.app.post('/paciente', json={
            'nome': 'João Silva',
            'email': 'joao@email.com',
            'cpf': '12345678901',
            'telefone': '11999999999',
            'senha': 'senha123'
        })
        self.assertEqual(response.status_code, 200)

    def test_criar_medico(self):
        response = self.app.post('/medico', json={
            'nome': 'Dra. Ana',
            'especialidade': 'Cardiologista',
            'email': 'ana@medico.com'
        })
        self.assertEqual(response.status_code, 200)

    def test_agendamento(self):
        self.test_criar_paciente()
        self.test_criar_medico()
        paciente = Paciente.query.first()
        medico = Medico.query.first()

        response = self.app.post('/agendar', json={
            'paciente_id': paciente.id,
            'medico_id': medico.id,
            'data': '2025-06-01',
            'horario': '14:00',
            'sintomas': 'Febre e dor no corpo'
        })
        self.assertEqual(response.status_code, 200)

    def test_atestado(self):
        response = self.app.post('/atestado', json={
            'paciente_nome': 'João Silva',
            'medico_nome': 'Dra. Ana',
            'tipo': 'Comparecimento'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data_hora', data)

if __name__ == '__main__':
    unittest.main()
