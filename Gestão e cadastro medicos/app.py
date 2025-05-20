from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'segredo'

def criar_banco():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, password TEXT, is_admin INTEGER
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT, especialidade TEXT, email TEXT
            )
        """)
        c.execute("SELECT * FROM usuarios WHERE username='admin'")
        if not c.fetchone():
            c.execute("INSERT INTO usuarios (username, password, is_admin) VALUES (?, ?, ?)", ('admin', '123', 1))
        conn.commit()

def admin_required(f):
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect('/login')
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        senha = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (user, senha))
            usuario = c.fetchone()
            if usuario:
                session['admin'] = bool(usuario[3])
                return redirect('/admin/medicos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin/medicos', methods=['GET', 'POST'])
@admin_required
def medicos():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        esp = request.form['especialidade']
        email = request.form['email']
        c.execute("INSERT INTO medicos (nome, especialidade, email) VALUES (?, ?, ?)", (nome, esp, email))
        conn.commit()
    c.execute("SELECT * FROM medicos")
    lista = c.fetchall()
    return render_template('medicos.html', medicos=lista)

@app.route('/admin/medicos/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        esp = request.form['especialidade']
        email = request.form['email']
        c.execute("UPDATE medicos SET nome=?, especialidade=?, email=? WHERE id=?", (nome, esp, email, id))
        conn.commit()
        return redirect('/admin/medicos')
    c.execute("SELECT * FROM medicos WHERE id=?", (id,))
    medico = c.fetchone()
    return render_template('editar.html', medico=medico)

@app.route('/admin/medicos/excluir/<int:id>')
@admin_required
def excluir(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM medicos WHERE id=?", (id,))
    conn.commit()
    return redirect('/admin/medicos')

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)
