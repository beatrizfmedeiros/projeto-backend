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
        dto = UsuarioCadastroDTO(
            nome=dados.get("nome"),
            email=dados.get("email"),
            senha=dados.get("senha"),
            telefone=dados.get("telefone"),
            cpf=dados.get("cpf"),
            endereco=dados.get("endereco"),
            referencia=dados.get("referencia")
        )
        try:
            dto.validate()  # Valida contrato sintático (Single Source of Truth)
            self.usuario_service.cadastrar(dto)
            return jsonify({"ok": True, "mensagem": f"Bem-vindo, {dto.nome}! Cadastro realizado."})
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception as e:
            err_msg = str(e).lower()
            if "unique" in err_msg or "integrity" in err_msg:
                return jsonify({"ok": False, "erro": "Este e-mail já está cadastrado."}), 409
            return jsonify({"ok": False, "erro": "Erro interno no servidor."}), 500

    def autenticar(self):
        dados = request.get_json(silent=True) or {}
        dto = UsuarioLoginDTO(
            email=dados.get("email"),
            senha=dados.get("senha")
        )
        try:
            dto.validate()  # Valida contrato sintático (Single Source of Truth)
            usuario = self.usuario_service.autenticar(dto)
            if usuario:
                session["usuario_id"] = usuario.id
                session["usuario_nome"] = usuario.nome
                return jsonify({"ok": True, "mensagem": f"Bem-vindo de volta, {usuario.nome}!", "nome": usuario.nome})
            return jsonify({"ok": False, "erro": "E-mail ou senha incorretos."}), 401
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400

    def logout(self):
        session.clear()
        return jsonify({"ok": True})

    def api_me(self):
        nome = session.get("usuario_nome")
        if nome:
            return jsonify({"logado": True, "nome": nome})
        return jsonify({"logado": False})
