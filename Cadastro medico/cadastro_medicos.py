import json
from typing import List, Dict


class SistemaCadastro:
    def __init__(self):
        self.medicos: List[Dict] = []
        self.usuarios: List[Dict] = []

    def cadastrar_medico(self, nome: str, username: str, senha: str) -> bool:
        if not (nome and username and senha):
            return False

        medico = {"nome": nome, "username": username, "senha": senha, "pacientes": 0}
        self.medicos.append(medico)

        usuario = {"username": username, "senha": senha, "role": "medico"}
        self.usuarios.append(usuario)

        return True

    def listar_medicos(self) -> List[Dict]:
        return self.medicos

    def atualizar_senha(self, username: str, nova_senha: str) -> bool:
        for medico in self.medicos:
            if medico["username"] == username:
                medico["senha"] = nova_senha
                break
        else:
            return False

        for usuario in self.usuarios:
            if usuario["username"] == username:
                usuario["senha"] = nova_senha
                return True
        return False

    def excluir_medico(self, username: str) -> bool:
        self.medicos = [m for m in self.medicos if m["username"] != username]
        self.usuarios = [u for u in self.usuarios if u["username"] != username]
        return True
