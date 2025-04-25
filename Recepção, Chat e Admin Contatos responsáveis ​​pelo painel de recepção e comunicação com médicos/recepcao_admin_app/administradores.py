from flask import Flask, jsonify

app = Flask(__name__)

administradores = [
    {
        "nome": "João Carlos",
        "telefone": "(11) 98765-4321",
        "email": "joao.carlos@hospital.com"
    },
    {
        "nome": "Ana Paula",
        "telefone": "(21) 91234-5678",
        "email": "ana.paula@hospital.com"
    },
    {
        "nome": "Roberto Silva",
        "telefone": "(31) 99876-5432",
        "email": "roberto.silva@hospital.com"
    }
]

@app.route("/administradores", methods=["GET"])
def get_administradores():
    return jsonify(administradores)

if __name__ == "__main__":
    app.run(debug=True)