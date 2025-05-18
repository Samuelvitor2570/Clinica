from flask import Flask, render_template, request
from datetime import datetime

# Inicializando o Flask
app = Flask(__name__)

# Dados de exemplo: Pacientes para cada médico
pacientes = {
    "Dra. Ana Silva": [
        {"nome": "Ricardo Santos", "email": "ricardo@gmail.com", "telefone": "123456789", "data": "2025-04-30", "hora": "08:00"},
        {"nome": "Fernanda Oliveira", "email": "fernanda@gmail.com", "telefone": "987654321", "data": "2025-05-01", "hora": "09:00"},
        {"nome": "Carlos Pereira", "email": "carlos@gmail.com", "telefone": "1122334455", "data": "2025-05-02", "hora": "10:00"},
        {"nome": "Juliana Costa", "email": "juliana@gmail.com", "telefone": "6677889900", "data": "2025-05-03", "hora": "13:00"},
    ],
    "Dra. Beatriz Lima": [
        {"nome": "Marcos Almeida", "email": "marcos@gmail.com", "telefone": "2233445566", "data": "2025-04-30", "hora": "09:00"},
        {"nome": "Laura Souza", "email": "laura@gmail.com", "telefone": "3344556677", "data": "2025-05-01", "hora": "10:00"},
        {"nome": "Lucas Mendes", "email": "lucas@gmail.com", "telefone": "4455667788", "data": "2025-05-02", "hora": "13:00"},
        {"nome": "Roberta Lima", "email": "roberta@gmail.com", "telefone": "5566778899", "data": "2025-05-03", "hora": "14:00"},
    ],
    "Dr. Carlos Mendes": [
        {"nome": "Gustavo Lima", "email": "gustavo@gmail.com", "telefone": "6677889900", "data": "2025-04-30", "hora": "10:00"},
        {"nome": "Tânia Oliveira", "email": "tania@gmail.com", "telefone": "7788990011", "data": "2025-05-01", "hora": "13:00"},
        {"nome": "Sergio Rodrigues", "email": "sergio@gmail.com", "telefone": "8899001122", "data": "2025-05-02", "hora": "14:00"},
        {"nome": "Beatriz Silva", "email": "beatriz@gmail.com", "telefone": "9900112233", "data": "2025-05-03", "hora": "16:00"},
    ]
}

# Função para ordenar pacientes por data e hora
def ordenar_pacientes(pacientes):
    return sorted(pacientes, key=lambda x: (datetime.strptime(x["data"], "%Y-%m-%d"), x["hora"]))

@app.route("/", methods=["GET", "POST"])
def medico_pacientes():
    # Recebe o nome do médico via GET (quando muda de médico) e verifica qual médico foi selecionado
    medico = request.args.get("medico", "Dra. Ana Silva")  # Começa com Dra. Ana Silva por padrão
    paciente_nome = request.form.get("nome", "").strip()

    # Ordena os pacientes do médico selecionado
    pacientes_do_medico = ordenar_pacientes(pacientes[medico])

    # Filtra pacientes por nome, se um nome for informado
    if paciente_nome:
        pacientes_do_medico = [p for p in pacientes_do_medico if paciente_nome.lower() in p["nome"].lower()]

    return render_template("medico_pacientes.html", 
                           medico=medico, 
                           pacientes=pacientes_do_medico, 
                           medico_list=["Dra. Ana Silva", "Dra. Beatriz Lima", "Dr. Carlos Mendes"],  # Ordem fixa dos médicos
                           paciente_nome=paciente_nome)

if __name__ == "__main__":
    app.run(debug=True)
