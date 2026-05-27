import hashlib
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
from backend.infra.storage.sqlite.sqlite_pedido_repository import SqlitePedidoRepository

bp = Blueprint("routes", __name__)

# Instanciação dos repositórios concretos
usuario_repo = SqliteUsuarioRepository()
pedido_repo = SqlitePedidoRepository()

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def usuario_logado():
    return session.get("usuario_nome")

# ─────────────────────────────────────────────
# Rotas – páginas
# ─────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("index.html", usuario=usuario_logado())

@bp.route("/login")
def login_page():
    if usuario_logado():
        return redirect(url_for("routes.index"))
    return render_template("login.html")

@bp.route("/cadastro")
def cadastro_page():
    if usuario_logado():
        return redirect(url_for("routes.index"))
    return render_template("cadastro.html")

@bp.route("/cardapio")
def cardapio_page():
    return render_template("cardapio.html", usuario=usuario_logado())

@bp.route("/sobre")
def sobre_page():
    return render_template("sobre.html", usuario=usuario_logado())

@bp.route("/carrinho")
def carrinho_page():
    item = (request.args.get("item") or "").strip()
    if not item:
        return redirect(url_for("routes.cardapio_page"))

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

@bp.route("/api/pedido", methods=["POST"])
def api_pedido():
    if not usuario_logado():
        return redirect(url_for("routes.login_page"))

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

    # resolve Id do usuário pelo nome
    usuario_id = usuario_repo.get_id_by_nome(usuario_nome)
    if not usuario_id:
        return redirect(url_for("routes.login_page"))

    # busca ou cria pedido aberto
    pedido = pedido_repo.get_open_pedido(usuario_id)
    if not pedido:
        pedido_id = pedido_repo.create_open_pedido(usuario_id)
    else:
        pedido_id = pedido["Id"]

    # adiciona item
    pedido_repo.add_item_to_pedido(pedido_id, item, item_foto, item_valor, qtd, personalizacao)

    # Mantém fluxo atual: volta para a página do item.
    return redirect(url_for("routes.carrinho_page", item=item) + f"&saved=1&qtd={qtd}")


# ─────────────────────────────────────────────
# API – cadastro
# ─────────────────────────────────────────────

@bp.route("/api/cadastro", methods=["POST"])
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
        usuario_repo.create_usuario(nome, telefone, email, cpf, endereco, referencia, senha_hash)
        return jsonify({"ok": True, "mensagem": f"Bem-vindo, {nome}! Cadastro realizado."})
    except Exception as e:
        err_msg = str(e).lower()
        if "unique" in err_msg or "integrity" in err_msg:
            return jsonify({"ok": False, "erro": "Este e-mail já está cadastrado."}), 409
        return jsonify({"ok": False, "erro": str(e)}), 500

# ─────────────────────────────────────────────
# API – login
# ─────────────────────────────────────────────

@bp.route("/api/login", methods=["POST"])
def api_login():
    dados = request.get_json(silent=True) or {}
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"ok": False, "erro": "Preencha e-mail e senha."}), 400

    usuario = usuario_repo.get_usuario_by_credentials(email, hash_senha(senha))

    if usuario:
        session["usuario_id"]   = usuario["Id"]
        session["usuario_nome"] = usuario["Nome"]
        return jsonify({"ok": True, "mensagem": f"Bem-vindo de volta, {usuario['Nome']}!", "nome": usuario["Nome"]})

    return jsonify({"ok": False, "erro": "E-mail ou senha incorretos."}), 401

# ─────────────────────────────────────────────
# API – logout / me
# ─────────────────────────────────────────────

@bp.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@bp.route("/meus-pedidos")
def meus_pedidos_page():
    if not usuario_logado():
        return redirect(url_for("routes.login_page"))

    usuario_nome = session.get("usuario_nome")

    usuario_id = usuario_repo.get_id_by_nome(usuario_nome)
    if not usuario_id:
        return redirect(url_for("routes.login_page"))

    itens = pedido_repo.get_open_pedido_items(usuario_id)

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

@bp.route("/api/me")
def api_me():
    if usuario_logado():
        return jsonify({"logado": True, "nome": session["usuario_nome"]})
    return jsonify({"logado": False})

# ─────────────────────────────────────────────
# API – remover item do pedido (ABERTO)
# ─────────────────────────────────────────────

@bp.route("/api/pedido_item/delete/<int:pedido_item_id>", methods=["POST"])
def api_pedido_item_delete(pedido_item_id: int):
    if not usuario_logado():
        return redirect(url_for("routes.login_page"))

    usuario_nome = session.get("usuario_nome")

    usuario_id = usuario_repo.get_id_by_nome(usuario_nome)
    if not usuario_id:
        return redirect(url_for("routes.login_page"))

    pedido_repo.delete_item_from_open_pedido(pedido_item_id, usuario_id)

    return redirect(url_for("routes.meus_pedidos_page"))

@bp.route("/api/pedido/finalizar", methods=["GET", "POST"])
def api_pedido_finalizar():
    if not usuario_logado():
        return redirect(url_for("routes.login_page"))

    usuario_nome = session.get("usuario_nome")

    usuario_id = usuario_repo.get_id_by_nome(usuario_nome)
    if not usuario_id:
        return redirect(url_for("routes.login_page"))

    pedido_repo.finalize_open_pedido(usuario_id)

    return redirect(url_for("routes.meus_pedidos_page"))
