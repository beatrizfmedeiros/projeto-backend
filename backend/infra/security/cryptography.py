import os
from cryptography.fernet import Fernet

class SymmetricCryptographer:
    def __init__(self, key: str = None):
        if not key:
            key = os.environ.get("ENCRYPTION_KEY")
            if not key:
                # Chave simétrica fallback base64 de 32 bytes segura para testes locais
                key = "dGVzdGVrZXlfdGVzdGVrZXlfdGVzdGVrZXlfdGVzdGVrZXk=" 
        
        self._fernet = Fernet(key.encode() if isinstance(key, str) else key)

    def encrypt(self, plain_text: str) -> str:
        """Criptografa um texto puro em uma string criptografada segura (base64)"""
        if not plain_text:
            return ""
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        """Descriptografa um token de volta em texto puro"""
        if not cipher_text:
            return ""
        try:
            return self._fernet.decrypt(cipher_text.encode()).decode()
        except Exception:
            # Em caso de falha (ex: dados legados sem criptografia), retorna o texto original intacto
            return cipher_text
