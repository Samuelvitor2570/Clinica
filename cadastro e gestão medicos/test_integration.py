import unittest
import os
from app import app, init_db
import tempfile

class TestMedicosIntegration(unittest.TestCase):
    def setUp(self):
        # Banco temporário para os testes
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login_admin(self):
        return self.client.get('/login', follow_redirects=True)

    def test_fluxo_completo_medico(self):
        self.login_admin()

        # Cadastro de médico
        response = self.client.post('/admin/medicos', data={
            'nome': 'Dr. Gabriel',
            'especialidade': 'Ortopedia'
        }, follow_redirects=True)
        self.assertIn(b'Dr. Gabriel', response.data)

        # Edição
        response = self.client.get('/admin/medicos')
        self.assertIn(b'Ortopedia', response.data)

        # Excluir
        # Primeiro, pegamos o ID do médico
        from sqlite3 import connect
        conn = connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM medicos WHERE nome='Dr. Gabriel'")
        medico_id = cursor.fetchone()[0]
        conn.close()

        # Agora excluímos
        response = self.client.get(f'/admin/medicos/excluir/{medico_id}', follow_redirects=True)
        self.assertNotIn(b'Dr. Gabriel', response.data)

if __name__ == '__main__':
    unittest.main()
