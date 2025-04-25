import unittest
from cadastro_medicos import SistemaCadastro


class TestSistemaCadastro(unittest.TestCase):

    def setUp(self):
        self.sistema = SistemaCadastro()

    def test_cadastrar_medico_valido(self):
        resultado = self.sistema.cadastrar_medico("Dr. João", "joao", "senha123")
        self.assertTrue(resultado)
        self.assertEqual(len(self.sistema.medicos), 1)
        self.assertEqual(self.sistema.medicos[0]["username"], "joao")

    def test_cadastrar_medico_invalido(self):
        resultado = self.sistema.cadastrar_medico("", "", "")
        self.assertFalse(resultado)
        self.assertEqual(len(self.sistema.medicos), 0)

    def test_listar_medicos(self):
        self.sistema.cadastrar_medico("Dra. Ana", "ana", "123")
        lista = self.sistema.listar_medicos()
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["nome"], "Dra. Ana")

    def test_atualizar_senha(self):
        self.sistema.cadastrar_medico("Dr. Carlos", "carlos", "oldpass")
        atualizado = self.sistema.atualizar_senha("carlos", "newpass")
        self.assertTrue(atualizado)
        self.assertEqual(self.sistema.medicos[0]["senha"], "newpass")

    def test_excluir_medico(self):
        self.sistema.cadastrar_medico("Dr. Pedro", "pedro", "senha")
        self.sistema.excluir_medico("pedro")
        self.assertEqual(len(self.sistema.medicos), 0)
        self.assertEqual(len(self.sistema.usuarios), 0)


if __name__ == '__main__':
    unittest.main()
