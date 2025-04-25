import unittest
from app import validar_agendamento, agenda
from datetime import datetime

class TestAgendamento(unittest.TestCase):
    def setUp(self):
        agenda.clear()

    def test_agendamento_disponivel(self):
        medico = "Dr. João"
        data = datetime(2025, 5, 1)
        self.assertTrue(validar_agendamento(medico, data))

    def test_agendamento_lotado(self):
        medico = "Dr. João"
        data = datetime(2025, 5, 1)
        for _ in range(6):
            validar_agendamento(medico, data)
            agenda[medico][data.strftime('%Y-%m-%d')] += 1
        self.assertFalse(validar_agendamento(medico, data))

if __name__ == "__main__":
    unittest.main()