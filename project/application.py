import sqlite3
import os
from flask import Flask, redirect, render_template, request, flash, url_for, session, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/deputados", methods=["GET", "POST"])
def deputados():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    db_cur = db.cursor()
    db_cur.execute('SELECT * FROM deputados')
    deputados = db_cur.fetchall()
    return render_template("deputados.html", deputados=deputados)
    db.close()

@app.route("/selecione_deputado", methods=["GET", "POST"])
def selecione_deputado():
    nomeDeputado = request.form.get("nomeCivil")
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    db_cur = db.cursor()
    db_cur.execute('SELECT * FROM deputados WHERE nomeCivil=:nomeDeputado', {'nomeDeputado': nomeDeputado})
    deputado = db_cur.fetchall()
    db_cur.execute('SELECT DISTINCT(votacoes.id), proposicoes.id AS idProp, proposicoes.urlInteiroTeor, proposicoes.ementa, proposicoes.descricaoSituacao, votacoes.data, resultadoVotacoes.voto FROM votacoes JOIN votacoesProposicoes ON votacoes.id = votacoesProposicoes.idVotacao JOIN proposicoes ON votacoesProposicoes.idProposicao = proposicoes.id JOIN resultadoVotacoes ON votacoes.id = resultadoVotacoes.idVotacao JOIN deputados ON resultadoVotacoes.idCandidato = deputados.id WHERE deputados.nomeCivil=:nomeDeputado ORDER BY votacoes.data ASC;', {'nomeDeputado': nomeDeputado})
    votacoes = db_cur.fetchall()
    return render_template("selecioneDeputado.html", deputado=deputado, votacoes=votacoes)
    db.close()

@app.route("/proposicoes", methods=["GET", "POST"])
def proposicoes():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    db_cur = db.cursor()
    db_cur.execute('SELECT * FROM proposicoes WHERE siglaTipo="PL"')
    proposicoes = db_cur.fetchall()
    return render_template("proposicoes.html", proposicoes=proposicoes)
    db.close()

@app.route("/meuscandidatos", methods=["GET", "POST"])
@login_required
def meuscandidatos():
    username = session["user_id"]
    if request.method == "POST":
        deputado = request.form.get("nomeCivil")
        db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
        db_cur = db.cursor()
        db_cur.execute('INSERT INTO deputadosUsers (idUser, deputado) VALUES (?, ?)', (username, deputado))
        db.commit()
        db_cur.execute('SELECT deputados.foto, deputados.nomeCivil, deputados.partido, deputados.escolaridade FROM deputadosUsers JOIN deputados ON deputadosUsers.deputado = deputados.nomeCivil WHERE idUser =:username', {'username': username})
        deputados = db_cur.fetchall()
        return render_template("meus_deputados.html", deputados=deputados)
        db.close()
    else:
        db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
        db_cur = db.cursor()
        db_cur.execute('SELECT deputados.foto, deputados.nomeCivil, deputados.partido, deputados.escolaridade FROM deputadosUsers JOIN deputados ON deputadosUsers.deputado = deputados.nomeCivil WHERE idUser =:username', {'username': username})
        deputados = db_cur.fetchall()
        return render_template("meus_deputados.html", deputados=deputados)
        db.close()

@app.route("/remove", methods=["POST"])
@login_required
def remove():
    username = session["user_id"]
    deputado = request.form.get("nomeCivil")
    db = sqlite3.connect('database.db', timeout=10)
    db.row_factory = sqlite3.Row
    db_cur = db.cursor()
    db_cur.execute('DELETE FROM deputadosUsers WHERE deputadosUsers.idUser =:username AND deputadosUsers.deputado =:deputado;', {'username': username, 'deputado': deputado})
    db.commit()
    db_cur.execute('SELECT deputados.foto, deputados.nomeCivil, deputados.partido, deputados.escolaridade FROM deputadosUsers JOIN deputados ON deputadosUsers.deputado = deputados.nomeCivil WHERE idUser =:username', {'username': username})
    deputados = db_cur.fetchall()
    return render_template("meus_deputados.html", deputados=deputados)
    db.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not username:
            msg = "must provide username"
            return render_template('status.html', msg=msg)
        elif not password:
            msg = "must provide password"
            return render_template('status.html', msg=msg)
        with sqlite3.connect('database.db') as db:
            db_cur = db.cursor()
            db_cur.execute('SELECT * FROM users WHERE username=:username', {'username': username})
            name = db_cur.fetchall()
            if len(name) != 1 or not check_password_hash(name[0][2], password):
                msg = "Invalid username and/or password"
                return render_template('status.html', msg = msg)
            session["user_id"] = name[0][0]
        return redirect("/meuscandidatos")
        db.close()
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'msg'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if not username:
            msg = "must provide username"
            return render_template('status.html', msg=msg)
        elif not password:
            msg = "must provide password"
            return render_template('status.html', msg=msg)
        elif not confirm_password:
            msg = "must confirm password"
            return render_template('status.html', msg=msg)
        elif password != confirm_password:
            msg = "passwords must match"
            return render_template('status.html', msg=msg)
        with sqlite3.connect('database.db') as db:
            db_cur = db.cursor()
            db_cur.execute('SELECT * FROM users WHERE username=:username', {'username': username})
            name = db_cur.fetchall()
            if len(name) != 0:
                msg = "Username already taken. Please choose another."
                return render_template('status.html', msg = msg)
            else:
                password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=4)
                db_cur.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, password))
                db.commit()
                msg = 'Registration successful'
        return render_template('status.html', msg=msg)
        db.close()
    else:
        return render_template('register.html')

if __name__ == '__main__':
    app.debug = True
    app.run()