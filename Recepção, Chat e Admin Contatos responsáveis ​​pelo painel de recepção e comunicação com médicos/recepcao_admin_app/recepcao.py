from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

atestados = []
chat = []
medicos = [{"nome": "Dr. João"}, {"nome": "Dra. Maria"}]

@app.route("/atestados", methods=["GET"])
def get_atestados():
    return jsonify(atestados)

@app.route("/atestados", methods=["POST"])
def add_atestado():
    data = request.get_json()
    atestados.append(data)
    return jsonify({"message": "Atestado adicionado com sucesso"}), 201

@app.route("/atestados/<int:index>", methods=["PUT"])
def update_atestado(index):
    if index >= len(atestados):
        return jsonify({"error": "Índice inválido"}), 404
    data = request.get_json()
    atestados[index] = data
    return jsonify({"message": "Atestado atualizado com sucesso"})

@app.route("/chat", methods=["GET"])
def get_chat():
    return jsonify(chat)

@app.route("/chat", methods=["POST"])
def post_chat():
    data = request.get_json()
    chat.append(data)
    return jsonify({"message": "Mensagem enviada"}), 201

@app.route("/medicos", methods=["GET"])
def get_medicos():
    return jsonify(medicos)

if __name__ == "__main__":
    app.run(debug=True)