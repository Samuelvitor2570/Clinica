import unittest
from administradores import listar_administradores, buscar_administrador_por_nome

class TestAdministradores(unittest.TestCase):
    
    def test_busca_existente(self):
        admin = buscar_administrador_por_nome("Ana Paula")
        self.assertIsNotNone(admin)
        self.assertEqual(admin["email"], "ana.paula@hospital.com")
    
    def test_busca_inexistente(self):
        admin = buscar_administrador_por_nome("Fulano")
        self.assertIsNone(admin)

if __name__ == "__main__":
    unittest.main()
