# /home/luigi/Projects/projeto-backend/backend/tests/test_admin_produto.py
import os
os.environ.setdefault('ENCRYPTION_KEY', '9vE2nWzU8WcF1VvD9YwR4G_8JxL1x3K2l5L7f7a1b2c=')
import json
import pytest
from backend.infra.server.app_factory import bootstrap_app
from backend.infra.security.jwt_auth import generate_token

@pytest.fixture
def client():
    """Create a Flask test client with a fresh app."""
    app = bootstrap_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def _ensure_user(user_id: int, name: str, email: str, role: str = "user"):
    """Insert or update a user in the SQLite test DB.
    The schema requires at least Nome, Email, Senha and role.
    """
    from backend.infra.db import get_db
    with get_db() as conn:
        # Insert a user if it doesn't exist; otherwise update role.
        conn.execute(
            "INSERT OR IGNORE INTO Usuarios (Id, Nome, Email, Senha, role) VALUES (?, ?, ?, ?, ?)",
            (user_id, name, email, "dummy_hash", role),
        )
        conn.execute(
            "UPDATE Usuarios SET role = ?, Nome = ?, Email = ? WHERE Id = ?",
            (role, name, email, user_id),
        )
        conn.commit()

def _make_auth_header(user_id: int, name: str, email: str, role: str = "user"):
    """Helper to create the Authorization header with a JWT token and ensure user exists."""
    _ensure_user(user_id, name, email, role)
    token = generate_token(user_id, name, email)
    return {"Authorization": f"Bearer {token}"}

def test_admin_can_create_product(client):
    admin_hdr = _make_auth_header(1, "Admin", "admin@example.com", role="admin")
    payload = {
        "nome": "Test Pizza",
        "preco": 49.90,
        "foto": "test.jpg",
        "descricao": "Delicious test pizza",
        "categoria": "Test",
        "tags": ["test", "pizza"],
        "ativo": True,
    }
    resp = client.post(
        "/api/admin/produtos",
        json=payload,
        headers=admin_hdr,
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["ok"] is True
    assert "id" in data
    return data["id"]

def test_non_admin_cannot_create_product(client):
    user_hdr = _make_auth_header(2, "User", "user@example.com")
    payload = {"nome": "Should Fail", "preco": 10.0}
    resp = client.post(
        "/api/admin/produtos",
        json=payload,
        headers=user_hdr,
    )
    assert resp.status_code == 403
    assert resp.get_json()["ok"] is False

def test_admin_can_update_product(client):
    prod_id = test_admin_can_create_product(client)
    admin_hdr = _make_auth_header(1, "Admin", "admin@example.com", role="admin")
    update_payload = {
        "nome": "Updated Pizza",
        "preco": 59.90,
        "tags": ["updated"],
        "ativo": False,
    }
    resp = client.put(
        f"/api/admin/produtos/{prod_id}",
        json=update_payload,
        headers=admin_hdr,
    )
    assert resp.status_code == 200
    assert resp.get_json()["ok"] is True

def test_non_admin_cannot_update_product(client):
    prod_id = test_admin_can_create_product(client)
    user_hdr = _make_auth_header(2, "User", "user@example.com")
    resp = client.put(
        f"/api/admin/produtos/{prod_id}",
        json={"nome": "X"},
        headers=user_hdr,
    )
    assert resp.status_code == 403

def test_admin_can_delete_product(client):
    prod_id = test_admin_can_create_product(client)
    admin_hdr = _make_auth_header(1, "Admin", "admin@example.com", role="admin")
    resp = client.delete(
        f"/api/admin/produtos/{prod_id}",
        headers=admin_hdr,
    )
    assert resp.status_code == 200
    assert resp.get_json()["ok"] is True

def test_non_admin_cannot_delete_product(client):
    prod_id = test_admin_can_create_product(client)
    user_hdr = _make_auth_header(2, "User", "user@example.com")
    resp = client.delete(
        f"/api/admin/produtos/{prod_id}",
        headers=user_hdr,
    )
    assert resp.status_code == 403
