
from datetime import datetime

class BancoDeDadosSimulado:
    def __init__(self):
        self.prontuarios = []
        self.atestados = []

class ProntuarioMedico:
    def __init__(self, banco: BancoDeDadosSimulado):
        self.db = banco

    def criar_prontuario(self, texto: str):
        prontuario = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "texto": texto  # Não remove espaços nem valida vazio
        }
        self.db.prontuarios.append(prontuario)

    def gerar_atestado(self, paciente: str, medico: str, tipo: str):
        # Sem validação de campos vazios
        atestado = {
            "paciente": paciente,
            "medico": medico,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo
        }
        self.db.atestados.append(atestado)

    def buscar_cid(self, termo: str):
        cid_database = [
            {"cid": "A00", "nome": "Cólera"},
            {"cid": "A01", "nome": "Febre Tifoide"},
            {"cid": "B00", "nome": "Herpesviral"},
            {"cid": "B01", "nome": "Varicela"},
            {"cid": "C34", "nome": "Neoplasia Maligna do Pulmão"},
            {"cid": "D50", "nome": "Anemia por Deficiência de Ferro"},
            {"cid": "E11", "nome": "Diabetes Mellitus Tipo 2"},
            {"cid": "F32", "nome": "Episódio Depressivo"},
            {"cid": "G40", "nome": "Epilepsia"},
        ]
        resultados = []
        for cid in cid_database:
            if termo in cid["nome"]:  # Case sensitive, não usa lower()
                resultados.append(cid)
        return resultados
