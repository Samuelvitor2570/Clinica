import unittest
from app import validar_agendamento, agenda

class TestAgendamento(unittest.TestCase):
    def setUp(self):
        agenda.clear()  # Limpa a agenda antes de cada teste

    def test_agendamento_abaixo_limite(self):
        medico = "Dr. Ana"
        data = "2025-04-25"
        for _ in range(5):
            agenda[(medico, data)].append({"nome": "Paciente", "idade": 30})
        self.assertTrue(validar_agendamento(medico, data))

    def test_agendamento_no_limite(self):
        medico = "Dr. Bruno"
        data = "2025-04-26"
        for _ in range(6):
            agenda[(medico, data)].append({"nome": "Paciente", "idade": 25})
        self.assertFalse(validar_agendamento(medico, data))

if __name__ == "__main__":
    unittest.main()
