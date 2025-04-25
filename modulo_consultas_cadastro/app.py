from flask import Flask, render_template, request, redirect
from datetime import datetime
app = Flask(__name__)

agenda = {}

def validar_agendamento(medico, data):
    data_str = data.strftime('%Y-%m-%d')
    if medico not in agenda:
        agenda[medico] = {}
    if data_str not in agenda[medico]:
        agenda[medico][data_str] = 0
    return agenda[medico][data_str] < 6

@app.route("/consultas", methods=["GET", "POST"])
def consultas():
    if request.method == "POST":
        nome = request.form["nome"]
        medico = request.form["medico"]
        data = datetime.strptime(request.form["data"], "%Y-%m-%d")
        if validar_agendamento(medico, data):
            data_str = data.strftime('%Y-%m-%d')
            agenda[medico][data_str] += 1
            return f"Consulta agendada com sucesso para {nome} com {medico} em {data_str}."
        else:
            return "Este médico já atingiu o limite de 6 pacientes para esta data."
    return render_template("formulario.html")

if __name__ == "__main__":
    app.run(debug=True)