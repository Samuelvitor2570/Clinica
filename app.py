from flask import Flask, request, render_template_string
from collections import defaultdict

import unittest

app = Flask(__name__)
agenda = defaultdict(list)

form_html = """
<h2>Agendamento de Consulta</h2>
<form method="post">
    Nome: <input type="text" name="nome" required><br>
    Idade: <input type="number" name="idade" required><br>
    Médico:
    <select name="medico">
        <option value="Dr. Ana">Dr. Ana</option>
        <option value="Dr. Bruno">Dr. Bruno</option>
        <option value="Dr. Carla">Dr. Carla</option>
    </select><br>
    Data: <input type="date" name="data" required><br>
    <input type="submit" value="Agendar">
</form>
{{ mensagem }}
"""

@app.route("/consultas", methods=["GET", "POST"])
def consultas():
    mensagem = ""
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        medico = request.form["medico"]
        data = request.form["data"]

        if validar_agendamento(medico, data):
            agenda[(medico, data)].append({"nome": nome, "idade": idade})
            mensagem = f"Consulta agendada com {medico} para o dia {data}."
        else:
            mensagem = f"Erro: {medico} já tem 6 pacientes agendados para o dia {data}."

    return render_template_string(form_html, mensagem=mensagem)

def validar_agendamento(medico, data):
    return len(agenda[(medico, data)]) < 6

# Testes unitários
class TestAgendamento(unittest.TestCase):
    def setUp(self):
        agenda.clear()

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
    # Você pode trocar isso por unittest.main() para rodar testes
    # ou por app.run() para rodar a aplicação
    print("Digite 'test' para rodar os testes ou qualquer outra coisa para iniciar o site:")
    escolha = input().strip()
    if escolha == "test":
        unittest.main(argv=[''], exit=False)
    else:
        app.run(debug=True)
