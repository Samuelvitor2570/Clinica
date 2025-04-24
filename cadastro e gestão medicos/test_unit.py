import unittest
import sqlite3
import os
from app import init_db

class TestMedicosDB(unittest.TestCase):

    def setUp(self):
        # Usa um banco separado para os testes
        self.test_db = 'test_database.db'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def test_insercao_medico(self):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicos (nome, especialidade) VALUES (?, ?)", ('João', 'Cardiologia'))
        conn.commit()
        cursor.execute("SELECT * FROM medicos WHERE nome=?", ('João',))
        medico = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(medico)
        self.assertEqual(medico[1], 'João')

    def test_exclusao_medico(self):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicos (nome, especialidade) VALUES (?, ?)", ('Maria', 'Pediatria'))
        conn.commit()
        cursor.execute("DELETE FROM medicos WHERE nome=?", ('Maria',))
        conn.commit()
        cursor.execute("SELECT * FROM medicos WHERE nome=?", ('Maria',))
        medico = cursor.fetchone()
        conn.close()
        self.assertIsNone(medico)

if __name__ == '__main__':
    unittest.main()
