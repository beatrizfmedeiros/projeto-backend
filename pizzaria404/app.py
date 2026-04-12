from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pizzaria404_dev_secret")
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "sistema.db")

# ─────────────────────────────────────────────
# Banco de dados
# ─────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome       TEXT    NOT NULL,
                Telefone   TEXT,
                Email      TEXT    NOT NULL UNIQUE,
                CPF        TEXT,
                Endereco   TEXT,
                Referencia TEXT,
                Senha      TEXT    NOT NULL,
                CriadoEm  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.commit()

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def usuario_logado():
    return session.get("usuario_nome")

# ─────────────────────────────────────────────
# Rotas – páginas
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", usuario=usuario_logado())

@app.route("/login")
def login_page():
    if usuario_logado():
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/cadastro")
def cadastro_page():
    if usuario_logado():
        return redirect(url_for("index"))
    return render_template("cadastro.html")

@app.route("/cardapio")
def cardapio_page():
    return render_template("cardapio.html", usuario=usuario_logado())

@app.route("/sobre")
def sobre_page():
    return render_template("sobre.html", usuario=usuario_logado())

# ─────────────────────────────────────────────
# API – cadastro
# ─────────────────────────────────────────────

@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    dados = request.get_json(silent=True) or {}

    for campo in ("nome", "email", "senha"):
        if not dados.get(campo, "").strip():
            return jsonify({"ok": False, "erro": f"Campo '{campo}' é obrigatório."}), 400

    nome       = dados["nome"].strip()
    email      = dados["email"].strip().lower()
    senha_hash = hash_senha(dados["senha"])
    telefone   = dados.get("telefone", "").strip()
    cpf        = dados.get("cpf", "").strip()
    endereco   = dados.get("endereco", "").strip()
    referencia = dados.get("referencia", "").strip()

    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO Usuarios (Nome, Telefone, Email, CPF, Endereco, Referencia, Senha)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nome, telefone, email, cpf, endereco, referencia, senha_hash),
            )
            conn.commit()
        return jsonify({"ok": True, "mensagem": f"Bem-vindo, {nome}! Cadastro realizado."})
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "erro": "Este e-mail já está cadastrado."}), 409
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)}), 500

# ─────────────────────────────────────────────
# API – login
# ─────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def api_login():
    dados = request.get_json(silent=True) or {}
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"ok": False, "erro": "Preencha e-mail e senha."}), 400

    with get_db() as conn:
        usuario = conn.execute(
            "SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?",
            (email, hash_senha(senha)),
        ).fetchone()

    if usuario:
        session["usuario_id"]   = usuario["Id"]
        session["usuario_nome"] = usuario["Nome"]
        return jsonify({"ok": True, "mensagem": f"Bem-vindo de volta, {usuario['Nome']}!", "nome": usuario["Nome"]})

    return jsonify({"ok": False, "erro": "E-mail ou senha incorretos."}), 401

# ─────────────────────────────────────────────
# API – logout / me
# ─────────────────────────────────────────────

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/me")
def api_me():
    if usuario_logado():
        return jsonify({"logado": True, "nome": session["usuario_nome"]})
    return jsonify({"logado": False})

# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("✅  Banco de dados pronto.")
    print("🍕  Pizzaria 404 → http://localhost:5000")
    app.run(debug=True)
