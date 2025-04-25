import unittest
from recepcao import app

class TestRecepcao(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.post("/chat", json={"autor": "Recepção", "mensagem": "Olá!"})
        self.client.post("/atestados", json={
            "paciente": "Carlos",
            "medico": "Dr. João",
            "data": "2024-04-25T10:00:00",
            "tipo": "Consulta",
            "assinatura": "Dr. João"
        })

    def test_get_atestados(self):
        response = self.client.get("/atestados")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_update_atestado(self):
        response = self.client.put("/atestados/0", json={
            "paciente": "Carlos Atualizado",
            "medico": "Dr. João",
            "data": "2024-04-25T10:00:00",
            "tipo": "Retorno",
            "assinatura": "Dr. João"
        })
        self.assertEqual(response.status_code, 200)

    def test_get_chat(self):
        response = self.client.get("/chat")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Recepção", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()