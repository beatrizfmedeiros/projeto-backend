from flask import request, jsonify, render_template, session, redirect, url_for
from backend.domain.dto.usuario_dto import UsuarioCadastroDTO, UsuarioLoginDTO
from backend.domain.service.usuario_service import UsuarioService

class UsuarioController:
    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service

    def index(self):
        nome = session.get("usuario_nome")
        return render_template("index.html", usuario=nome)

    def login_page(self):
        if session.get("usuario_nome"):
            return redirect(url_for("routes.index"))
        return render_template("login.html")

    def cadastro_page(self):
        if session.get("usuario_nome"):
            return redirect(url_for("routes.index"))
        return render_template("cadastro.html")

    def cadastrar(self):
        dados = request.get_json(silent=True) or {}
        for campo in ("nome", "email", "senha"):
            if not dados.get(campo, "").strip():
                return jsonify({"ok": False, "erro": f"Campo '{campo}' é obrigatório."}), 400

        dto = UsuarioCadastroDTO(
            nome=dados["nome"].strip(),
            email=dados["email"].strip().lower(),
            senha=dados["senha"],
            telefone=dados.get("telefone", "").strip(),
            cpf=dados.get("cpf", "").strip(),
            endereco=dados.get("endereco", "").strip(),
            referencia=dados.get("referencia", "").strip()
        )
        try:
            self.usuario_service.cadastrar(dto)
            return jsonify({"ok": True, "mensagem": f"Bem-vindo, {dto.nome}! Cadastro realizado."})
        except Exception as e:
            err_msg = str(e).lower()
            if "unique" in err_msg or "integrity" in err_msg:
                return jsonify({"ok": False, "erro": "Este e-mail já está cadastrado."}), 409
            return jsonify({"ok": False, "erro": str(e)}), 500

    def autenticar(self):
        dados = request.get_json(silent=True) or {}
        email = dados.get("email", "").strip().lower()
        senha = dados.get("senha", "")
        if not email or not senha:
            return jsonify({"ok": False, "erro": "Preencha e-mail e senha."}), 400

        dto = UsuarioLoginDTO(email, senha)
        usuario = self.usuario_service.autenticar(dto)

        if usuario:
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return jsonify({"ok": True, "mensagem": f"Bem-vindo de volta, {usuario.nome}!", "nome": usuario.nome})

        return jsonify({"ok": False, "erro": "E-mail ou senha incorretos."}), 401

    def logout(self):
        session.clear()
        return jsonify({"ok": True})

    def api_me(self):
        nome = session.get("usuario_nome")
        if nome:
            return jsonify({"logado": True, "nome": nome})
        return jsonify({"logado": False})
