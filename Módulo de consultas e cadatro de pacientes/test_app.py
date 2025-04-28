import unittest
from app import app, validar_email, validar_telefone, eh_dia_util, eh_horario_valido, paciente_cadastrado, pacientes, agendamentos

class TestApp(unittest.TestCase):

    def test_validar_telefone_valido(self):
        """Testa validação de telefone válido."""
        self.assertTrue(validar_telefone('123456789'))

    def test_validar_telefone_invalido(self):
        """Testa validação de telefone inválido."""
        self.assertFalse(validar_telefone('abc'))

    def test_validar_email_valido(self):
        """Testa validação de email válido."""
        self.assertTrue(validar_email('teste@exemplo.com'))

    def test_validar_email_invalido(self):
        """Testa validação de email inválido."""
        self.assertFalse(validar_email('email_invalido'))

    def test_eh_dia_util_segunda(self):
        """Testa se segunda-feira é dia útil."""
        self.assertTrue(eh_dia_util('2025-04-28'))  # Segunda-feira

    def test_eh_dia_util_domingo(self):
        """Testa se domingo não é dia útil."""
        self.assertFalse(eh_dia_util('2025-04-27'))  # Domingo

    def test_eh_horario_valido_ok(self):
        """Testa validação de horário permitido."""
        self.assertTrue(eh_horario_valido('08:00'))

    def test_eh_horario_valido_invalido(self):
        """Testa validação de horário não permitido."""
        self.assertFalse(eh_horario_valido('11:00'))

    def test_paciente_cadastrado_true(self):
        """Testa verificação de paciente cadastrado."""
        pacientes.append({'nome': 'Teste', 'email': 'teste@exemplo.com', 'telefone': '123456789'})
        self.assertTrue(paciente_cadastrado('teste@exemplo.com'))
        pacientes.clear()

    def test_paciente_cadastrado_false(self):
        """Testa verificação de paciente não cadastrado."""
        self.assertFalse(paciente_cadastrado('nao_existe@exemplo.com'))

    # Adicione os outros testes aqui...

if __name__ == '__main__':
    unittest.main()