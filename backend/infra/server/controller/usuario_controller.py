from flask import request, jsonify, render_template, session, redirect, url_for
from backend.domain.dto.usuario_dto import UsuarioCadastroDTO, UsuarioLoginDTO
from backend.domain.service.usuario_service import UsuarioService
from backend.infra.security.jwt_auth import generate_token

class UsuarioController:
    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service



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
            
            # Autentica automaticamente após o cadastro para obter o objeto do usuário (com o ID gerado)
            login_dto = UsuarioLoginDTO(email=dto.email, senha=dto.senha)
            usuario = self.usuario_service.autenticar(login_dto)
            
            token = None
            if usuario:
                session["usuario_id"] = usuario.id
                session["usuario_nome"] = usuario.nome
                token = generate_token(usuario.id, usuario.nome, usuario.email)

            return jsonify({
                "ok": True,
                "mensagem": f"Bem-vindo, {dto.nome}! Cadastro realizado.",
                "nome": dto.nome,
                "token": token
            })
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
                # Gera o token de API
                token = generate_token(usuario.id, usuario.nome, usuario.email)
                return jsonify({
                    "ok": True,
                    "mensagem": f"Bem-vindo de volta, {usuario.nome}!",
                    "nome": usuario.nome,
                    "token": token
                })
            return jsonify({"ok": False, "erro": "E-mail ou senha incorretos."}), 401
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400

    def logout(self):
        session.clear()
        return jsonify({"ok": True})

    def api_me(self):
        # 1. Tenta obter o usuário via JWT Bearer Token no cabeçalho
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                from backend.infra.security.jwt_auth import decode_token
                payload = decode_token(token)
                return jsonify({
                    "logado": True,
                    "nome": payload["nome"],
                    "email": payload["email"],
                    "metodo": "JWT"
                })
            except Exception:
                pass

        # 2. Fallback para Sessão clássica por cookies
        nome = session.get("usuario_nome")
        if nome:
            return jsonify({
                "logado": True,
                "nome": nome,
                "metodo": "Session"
            })

        return jsonify({"logado": False})
