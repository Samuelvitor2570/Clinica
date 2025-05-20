import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("database.json")

def carregar_dados():
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"prontuarios": [], "atestados": []}

def salvar_dados(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def criar_prontuario(paciente, medico, texto):
    if not paciente or not medico or not texto:
        raise ValueError("Todos os campos são obrigatórios.")
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    prontuario = {
        "data": data,
        "paciente": paciente,
        "medico": medico,
        "texto": texto
    }
    dados = carregar_dados()
    dados["prontuarios"].append(prontuario)
    salvar_dados(dados)
    return prontuario

def gerar_atestado(paciente, medico, tipo):
    if not paciente or not medico or not tipo:
        raise ValueError("Todos os campos são obrigatórios.")
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    atestado = {
        "data": data,
        "paciente": paciente,
        "medico": medico,
        "tipo": tipo
    }
    dados = carregar_dados()
    dados["atestados"].append(atestado)
    salvar_dados(dados)
    return atestado
