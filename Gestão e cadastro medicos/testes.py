import unittest
from app import app, criar_banco
import sqlite3

class TestApp(unittest.TestCase):
    def setUp(self):
        criar_banco()
        self.app = app.test_client()
        self.app.testing = True

    def login_admin(self):
        return self.app.post('/login', data=dict(username='admin', password='123'), follow_redirects=True)

    def test_login_sucesso(self):
        res = self.login_admin()
        self.assertIn('Cadastro de Médicos', res.get_data(as_text=True))

    def test_login_falha(self):
        res = self.app.post('/login', data=dict(username='admin', password='errado'))
        self.assertNotIn('Cadastro de Médicos', res.get_data(as_text=True))

    def test_cadastro_medico(self):
        self.login_admin()
        res = self.app.post('/admin/medicos', data=dict(nome='Dr. Teste', especialidade='Cardiologia', email='teste@ex.com'), follow_redirects=True)
        self.assertIn('Dr. Teste', res.get_data(as_text=True))

    def test_editar_medico(self):
        self.login_admin()
        self.app.post('/admin/medicos', data=dict(nome='Dr. Editar', especialidade='Ortopedia', email='edit@ex.com'), follow_redirects=True)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE nome='Dr. Editar'")
        id_medico = c.fetchone()[0]
        res = self.app.post(f'/admin/medicos/editar/{id_medico}', data=dict(nome='Dr. Editado', especialidade='Neuro', email='novo@ex.com'), follow_redirects=True)
        self.assertIn('Dr. Editado', res.get_data(as_text=True))

    def test_excluir_medico(self):
        self.login_admin()
        self.app.post('/admin/medicos', data=dict(nome='Dr. Delete', especialidade='Pediatria', email='del@ex.com'), follow_redirects=True)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id FROM medicos WHERE nome='Dr. Delete'")
        id_medico = c.fetchone()[0]
        res = self.app.get(f'/admin/medicos/excluir/{id_medico}', follow_redirects=True)
        self.assertNotIn('Dr. Delete', res.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
