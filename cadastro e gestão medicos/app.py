from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Criação do banco se não existir
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# AQUI: rota que lista os médicos
@app.route('/admin/medicos')
def listar_medicos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM medicos')
    medicos = cursor.fetchall()
    conn.close()
    return render_template('medicos.html', medicos=medicos)


# Inicializa o banco na primeira vez
with app.app_context():
    init_db()

# Simulação de login automático (admin)
@app.route('/login')
def login():
    session['usuario'] = 'admin'
    session['tipo'] = 'admin'
    return redirect(url_for('medicos'))

# Página principal: cadastro, visualização, exclusão
@app.route('/admin/medicos', methods=['GET', 'POST'])
def medicos():
    if session.get('tipo') != 'admin':
        return "Acesso negado. Apenas administradores."

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Cadastro
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        cursor.execute("INSERT INTO medicos (nome, especialidade) VALUES (?, ?)", (nome, especialidade))
        conn.commit()

    # Lista de médicos
    cursor.execute("SELECT * FROM medicos")
    lista_medicos = cursor.fetchall()
    conn.close()

    return render_template('medicos.html', medicos=lista_medicos)

# Excluir médico
@app.route('/admin/medicos/excluir/<int:id>')
def excluir_medico(id):
    if session.get('tipo') != 'admin':
        return "Acesso negado."

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('medicos'))

# Editar médico
@app.route('/admin/medicos/editar/<int:id>', methods=['GET', 'POST'])
def editar_medico(id):
    if session.get('tipo') != 'admin':
        return "Acesso negado."

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        cursor.execute("UPDATE medicos SET nome=?, especialidade=? WHERE id=?", (nome, especialidade, id))
        conn.commit()
        conn.close()
        return redirect(url_for('medicos'))

    cursor.execute("SELECT * FROM medicos WHERE id=?", (id,))
    medico = cursor.fetchone()
    conn.close()
    return render_template('editar_medico.html', medico=medico)

if __name__ == '__main__':
    app.run(debug=True)
