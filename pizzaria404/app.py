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

        # Pedido "aberto" do usuário (um pedido agregado que acumula itens)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Pedidos (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                UsuarioId INTEGER NOT NULL,
                Status    TEXT    NOT NULL DEFAULT 'ABERTO',
                CriadoEm   TEXT   DEFAULT (datetime('now')),
                FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
            )
        """)

        # Itens do pedido
        conn.execute("""
            CREATE TABLE IF NOT EXISTS PedidoItens (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                PedidoId  INTEGER NOT NULL,
                ItemNome   TEXT NOT NULL,
                ItemFoto   TEXT,
                ItemValor  REAL NOT NULL,
                Quantidade INTEGER NOT NULL DEFAULT 1,
                Observacao TEXT,
                CriadoEm   TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (PedidoId) REFERENCES Pedidos(Id)
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

@app.route("/carrinho")
def carrinho_page():
    item = (request.args.get("item") or "").strip()
    if not item:
        return redirect(url_for("cardapio_page"))

    valores = {

        "Calabresa": 39.90,
        "Mussarela": 34.90,
        "Quatro Queijos": 49.90,
        "Brigadeiro": 29.90,
        "M&M": 32.90,
        "Romeu & Julieta": 31.90,
        "Coxinha": 25.90,
        "Vulcão": 45.90,
        "Nutella": 37.90,
    }

    valor = valores.get(item, 29.90)
    return render_template(
        "carrinho.html",
        usuario=usuario_logado(),
        item_nome=item,
        item_valor=f"{valor:.2f}".replace(".", ","),
    )

@app.route("/api/pedido", methods=["POST"])
def api_pedido():
    if not usuario_logado():
        return redirect(url_for("login_page"))

    usuario_nome = session.get("usuario_nome")
    item = (request.form.get("item") or "").strip()
    personalizacao = (request.form.get("personalizacao") or "").strip()
    quantidade = request.form.get("quantidade", "1").strip()

    # Validação quantidade
    try:
        qtd = int(quantidade)
        if qtd < 1:
            qtd = 1
    except Exception:
        qtd = 1

    # Preço e foto (foto baseada no que já existe no cardápio)
    valores = {
        "Calabresa": 39.90,
        "Mussarela": 34.90,
        "Quatro Queijos": 49.90,
        "Brigadeiro": 29.90,
        "M&M": 32.90,
        "Romeu & Julieta": 31.90,
        "Coxinha": 25.90,
        "Vulcão": 45.90,
        "Nutella": 37.90,
    }

    fotos = {
        "Calabresa": "calabresa.jpeg",
        "Mussarela": "mussarela.jpeg",
        "Quatro Queijos": "4queijos.jpg",
        "Brigadeiro": "brigadeiro.jpg",
        "M&M": "mem.jpg",
        "Romeu & Julieta": "roju.jpg",
        "Coxinha": "espcoxinha.jpg",
        "Vulcão": "espvulcao.jpg",
        "Nutella": "espnutella.jpg",
    }

    item_valor = valores.get(item, 29.90)
    item_foto = fotos.get(item, "")

    with get_db() as conn:
        # resolve Id do usuário pelo nome salvo na sessão (já que temos usuario_nome)
        usuario = conn.execute("SELECT Id FROM Usuarios WHERE Nome = ?", (usuario_nome,)).fetchone()
        if not usuario:
            return redirect(url_for("login_page"))

        usuario_id = usuario["Id"]

        # busca pedido aberto
        pedido = conn.execute(
            "SELECT * FROM Pedidos WHERE UsuarioId = ? AND Status = 'ABERTO' ORDER BY Id DESC LIMIT 1",
            (usuario_id,),
        ).fetchone()

        if not pedido:
            cur = conn.execute(
                "INSERT INTO Pedidos (UsuarioId, Status) VALUES (?, 'ABERTO')",
                (usuario_id,),
            )
            pedido_id = cur.lastrowid
        else:
            pedido_id = pedido["Id"]

        conn.execute(
            """
                INSERT INTO PedidoItens (PedidoId, ItemNome, ItemFoto, ItemValor, Quantidade, Observacao)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
            (pedido_id, item, item_foto, float(item_valor), int(qtd), personalizacao),
        )

        conn.commit()

    # Mantém fluxo atual: volta para a página do item.
    return redirect(url_for("carrinho_page", item=item) + f"&saved=1&qtd={qtd}")


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

@app.route("/meus-pedidos")
def meus_pedidos_page():
    if not usuario_logado():
        return redirect(url_for("login_page"))

    usuario_nome = session.get("usuario_nome")

    with get_db() as conn:
        usuario = conn.execute("SELECT Id FROM Usuarios WHERE Nome = ?", (usuario_nome,)).fetchone()
        if not usuario:
            return redirect(url_for("login_page"))

        usuario_id = usuario["Id"]

        itens = conn.execute(
            """
            SELECT pi.ItemNome as nome,
                   pi.ItemFoto as foto,
                   pi.ItemValor as valor,
                   pi.Quantidade as quantidade,
                   pi.Observacao as observacao
            FROM PedidoItens pi
            JOIN Pedidos p ON p.Id = pi.PedidoId
            WHERE p.UsuarioId = ? AND p.Status = 'ABERTO'
            ORDER BY pi.Id DESC
            """,
            (usuario_id,),
        ).fetchall()

    total = 0.0
    itens_out = []
    for it in itens:
        valor = float(it["valor"])
        quantidade = int(it["quantidade"])
        subtotal = valor * quantidade
        total += subtotal
        itens_out.append({
            "nome": it["nome"],
            "foto": it["foto"],
            "valor": valor,
            "quantidade": quantidade,
            "observacao": it["observacao"],
            "valor_formatado": f"{subtotal:.2f}".replace('.', ','),
        })

    total_formatado = f"{total:.2f}".replace('.', ',')

    return render_template(
        "meus_pedidos.html",
        usuario=usuario_nome,
        itens=itens_out,
        total_formatado=total_formatado,
    )


@app.route("/api/me")
def api_me():
    if usuario_logado():
        return jsonify({"logado": True, "nome": session["usuario_nome"]})
    return jsonify({"logado": False})

# ─────────────────────────────────────────────
# API – remover item do pedido (ABERTO)
# ─────────────────────────────────────────────

@app.route("/api/pedido_item/delete/<int:pedido_item_id>", methods=["POST"])
def api_pedido_item_delete(pedido_item_id: int):
    if not usuario_logado():
        return redirect(url_for("login_page"))

    usuario_nome = session.get("usuario_nome")

    with get_db() as conn:
        usuario = conn.execute("SELECT Id FROM Usuarios WHERE Nome = ?", (usuario_nome,)).fetchone()
        if not usuario:
            return redirect(url_for("login_page"))

        usuario_id = usuario["Id"]

        # delete apenas se o item pertencer a um pedido ABERTO do usuário logado
        conn.execute(
            """
            DELETE FROM PedidoItens
            WHERE Id = ?
              AND PedidoId IN (
                SELECT Id FROM Pedidos
                WHERE UsuarioId = ? AND Status = 'ABERTO'
              )
            """,
            (pedido_item_id, usuario_id),
        )
        conn.commit()

    return redirect(url_for("meus_pedidos_page"))


@app.route("/api/pedido/finalizar", methods=["GET", "POST"])
def api_pedido_finalizar():
    # “Finalizar pedido” apenas marca o pedido ABERTO como finalizado.
    if not usuario_logado():
        return redirect(url_for("login_page"))

    usuario_nome = session.get("usuario_nome")

    with get_db() as conn:
        usuario = conn.execute("SELECT Id FROM Usuarios WHERE Nome = ?", (usuario_nome,)).fetchone()
        if not usuario:
            return redirect(url_for("login_page"))

        usuario_id = usuario["Id"]

        conn.execute(
            """
            UPDATE Pedidos
            SET Status = 'FINALIZADO'
            WHERE UsuarioId = ? AND Status = 'ABERTO'
            """,
            (usuario_id,),
        )
        conn.commit()

    return redirect(url_for("meus_pedidos_page"))


# ─────────────────────────────────────────────


if __name__ == "__main__":
    init_db()
    print("✅  Banco de dados pronto.")
    print("🍕  Pizzaria 404 → http://localhost:5000")
    app.run(debug=True)

