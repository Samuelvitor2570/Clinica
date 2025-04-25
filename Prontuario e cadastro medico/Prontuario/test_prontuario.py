
import unittest
from prontuario import BancoDeDadosSimulado, ProntuarioMedico

class TestProntuarioComErros(unittest.TestCase):
    def setUp(self):
        self.banco = BancoDeDadosSimulado()
        self.sistema = ProntuarioMedico(self.banco)

    def test_criar_prontuario_sem_texto(self):
        self.sistema.criar_prontuario("")  # Nenhum erro esperado, mas deveria

    def test_gerar_atestado_sem_nome(self):
        self.sistema.gerar_atestado("", "", "médico")  # Nenhum erro esperado, mas deveria

    def test_buscar_cid_case_sensitive(self):
        resultados = self.sistema.buscar_cid("diabetes")  # Não encontra, pois é case sensitive
        self.assertEqual(resultados, [])

if __name__ == '__main__':
    unittest.main()
