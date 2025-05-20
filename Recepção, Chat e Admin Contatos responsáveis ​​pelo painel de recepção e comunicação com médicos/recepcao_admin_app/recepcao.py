from datetime import datetime

# Lista de médicos disponíveis
medicos = [
    {"nome": "Dr. João"},
    {"nome": "Dra. Maria"},
]

# Lista de atestados
atestados = []

# Lista de mensagens do chat
chat = []

# --- Atestados ---

def adicionar_atestado(paciente, medico, data, tipo, assinatura):
    atestado = {
        "paciente": paciente,
        "medico": medico,
        "data": data,
        "tipo": tipo,
        "assinatura": assinatura
    }
    atestados.append(atestado)
    print("✔️ Atestado adicionado com sucesso.")

def listar_atestados():
    for i, a in enumerate(atestados):
        print(f"\nAtestado #{i}")
        print(f"Paciente: {a['paciente']}")
        print(f"Médico: {a['medico']}")
        print(f"Data: {a['data']}")
        print(f"Tipo: {a['tipo']}")
        print(f"Assinatura: {a['assinatura']}")
        print("-" * 40)

def editar_atestado(index, paciente=None, medico=None, data=None, tipo=None, assinatura=None):
    if 0 <= index < len(atestados):
        if paciente: atestados[index]["paciente"] = paciente
        if medico: atestados[index]["medico"] = medico
        if data: atestados[index]["data"] = data
        if tipo: atestados[index]["tipo"] = tipo
        if assinatura: atestados[index]["assinatura"] = assinatura
        print("✔️ Atestado atualizado com sucesso.")
    else:
        print("❌ Índice de atestado inválido.")

# --- Chat ---

def enviar_mensagem(autor, mensagem):
    chat.append({"autor": autor, "mensagem": mensagem})
    print(f"✔️ Mensagem enviada por {autor}.")

def listar_chat():
    print("\n=== Histórico do Chat ===")
    for msg in chat:
        print(f"{msg['autor']}: {msg['mensagem']}")
    print("-" * 40)

# --- Médicos ---

def listar_medicos():
    print("\n=== Médicos Cadastrados ===")
    for m in medicos:
        print(f"- {m['nome']}")
    print("-" * 40)

# Testes manuais
if __name__ == "__main__":
    listar_medicos()
    enviar_mensagem("Recepção", "Bom dia, equipe!")
    enviar_mensagem("Médico", "Bom dia! Algum paciente chegou?")
    listar_chat()

    adicionar_atestado("Carlos", "Dr. João", "2025-05-20 10:00", "Consulta", "Dr. João")
    listar_atestados()
    editar_atestado(0, paciente="Carlos Silva", tipo="Retorno")
    listar_atestados()
