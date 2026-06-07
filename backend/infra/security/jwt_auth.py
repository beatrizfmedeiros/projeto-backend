import os
import datetime
import functools
import jwt
from flask import request, session, jsonify, g, redirect, url_for

SECRET_KEY = os.environ.get("SECRET_KEY", "pizzaria404_dev_secret_key_secure_32bytes")

def generate_token(usuario_id: int, nome: str, email: str) -> str:
    """Gera um token JWT com validade de 24 horas"""
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "nome": nome,
        "email": email,
        "exp": now + datetime.timedelta(hours=24),
        "iat": now
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    """Decodifica e valida o token JWT. Levanta exceções caso inválido/expirado."""
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

def auth_required(f):
    """Decorador híbrido que suporta JWT Bearer Header (API) e Cookie Session (Templates)"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # 1. Tenta autenticação via JWT Bearer Token (para requisições de API REST)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token)
                # Injeta dados mínimos de contexto para o fluxo
                from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
                usuario = SqliteUsuarioRepository().get_by_name(payload["nome"])
                if usuario:
                    g.current_user = usuario
                    g.auth_method = "JWT"
                    return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"ok": False, "erro": "Token expirado. Efetue login novamente."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"ok": False, "erro": "Token de autenticação inválido."}), 401

        # 2. Fallback: Autenticação clássica via cookies de sessão (para renderização de templates Jinja2)
        usuario_nome = session.get("usuario_nome")
        if usuario_nome:
            from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
            usuario = SqliteUsuarioRepository().get_by_nome(usuario_nome)
            if usuario:
                g.current_user = usuario
                g.auth_method = "Session"
                return f(*args, **kwargs)

        # 3. Falha Geral: Sempre retorna JSON 401
        return jsonify({
            "ok": False,
            "erro": "Autenticação necessária. Envie o cabeçalho 'Authorization: Bearer <token_jwt>'."
        }), 401
    return decorated


def admin_required(f):
    """Decorator that ensures the current user has role 'admin'. Returns 403 otherwise."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        user = getattr(g, 'current_user', None)
        if user and getattr(user, 'role', None) == 'admin':
            return f(*args, **kwargs)
        return jsonify({"ok": False, "erro": "Permissão de administrador necessária."}), 403
    return wrapper
