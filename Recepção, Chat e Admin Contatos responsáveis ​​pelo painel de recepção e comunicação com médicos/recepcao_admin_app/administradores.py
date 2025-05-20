# Lista de administradores
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

def listar_administradores():
    """Imprime todos os administradores cadastrados."""
    for admin in administradores:
        print(f"Nome: {admin['nome']}")
        print(f"Telefone: {admin['telefone']}")
        print(f"Email: {admin['email']}")
        print("-" * 40)

def buscar_administrador_por_nome(nome):
    """Retorna os dados de um administrador pelo nome."""
    for admin in administradores:
        if admin["nome"].lower() == nome.lower():
            return admin
    return None

# Teste manual simples
if __name__ == "__main__":
    print("=== Lista de Administradores ===")
    listar_administradores()

    print("\n=== Buscar um administrador ===")
    nome_busca = "Ana Paula"
    admin = buscar_administrador_por_nome(nome_busca)
    if admin:
        print(f"Encontrado: {admin['nome']} - {admin['telefone']} - {admin['email']}")
    else:
        print(f"Administrador '{nome_busca}' não encontrado.")
