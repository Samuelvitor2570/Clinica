import unittest
from main import app

class MedicoPacientesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_listar_pacientes(self):
        response = self.app.get('/medico/pacientes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Carlos Silva', response.data)
        self.assertIn(b'Ana Costa', response.data)
        self.assertNotIn(b'JosÃ© Santos', response.data)  # paciente do outro médico

    def test_busca_paciente(self):
        response = self.app.get('/medico/pacientes?busca=ana')
        self.assertIn(b'Ana Costa', response.data)
        self.assertNotIn(b'Carlos Silva', response.data)

if __name__ == '__main__':
    unittest.main()
