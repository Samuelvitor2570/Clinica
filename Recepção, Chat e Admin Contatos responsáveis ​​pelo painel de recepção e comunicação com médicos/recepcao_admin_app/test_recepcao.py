import unittest
import recepcao

class TestRecepcao(unittest.TestCase):

    def setUp(self):
        recepcao.atestados.clear()
        recepcao.chat.clear()

    def test_adicionar_e_listar_atestado(self):
        recepcao.adicionar_atestado("Joana", "Dr. João", "2025-05-20 10:00", "Consulta", "Dr. João")
        self.assertEqual(len(recepcao.atestados), 1)
        self.assertEqual(recepcao.atestados[0]["paciente"], "Joana")

    def test_editar_atestado(self):
        recepcao.adicionar_atestado("Carlos", "Dr. João", "2025-05-20 10:00", "Consulta", "Dr. João")
        recepcao.editar_atestado(0, paciente="Carlos Silva", tipo="Emergência")
        self.assertEqual(recepcao.atestados[0]["paciente"], "Carlos Silva")
        self.assertEqual(recepcao.atestados[0]["tipo"], "Emergência")

    def test_enviar_e_listar_chat(self):
        recepcao.enviar_mensagem("Recepção", "Olá")
        self.assertEqual(len(recepcao.chat), 1)
        self.assertEqual(recepcao.chat[0]["mensagem"], "Olá")

if __name__ == "__main__":
    unittest.main()
