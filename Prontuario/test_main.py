import unittest
from main import criar_prontuario, gerar_atestado, salvar_dados

class TestSistemaMedico(unittest.TestCase):

    def setUp(self):
        salvar_dados({"prontuarios": [], "atestados": []})

    def test_criar_prontuario_valido(self):
        resultado = criar_prontuario("João", "Dr. Ana", "Consulta de rotina")
        self.assertEqual(resultado["paciente"], "João")
        self.assertEqual(resultado["medico"], "Dr. Ana")
        self.assertIn("data", resultado)

    def test_criar_prontuario_invalido(self):
        with self.assertRaises(ValueError):
            criar_prontuario("", "Dr. Ana", "Consulta")

    def test_gerar_atestado_valido(self):
        resultado = gerar_atestado("Maria", "Dr. José", "médico")
        self.assertEqual(resultado["paciente"], "Maria")
        self.assertEqual(resultado["tipo"], "médico")

    def test_gerar_atestado_invalido(self):
        with self.assertRaises(ValueError):
            gerar_atestado("", "Dr. José", "comparecimento")

if __name__ == '__main__':
    unittest.main()
