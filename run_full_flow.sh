#!/usr/bin/env bash
set -euo pipefail
BASE="http://127.0.0.1:5000"
# Register
REG=$(curl -s -X POST "$BASE/api/cadastro" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Luigi","email":"luigi@example.com","senha":"senha123","telefone":"99999-9999","cpf":"12345678900","endereco":"Rua das Pizzas, 42","referencia":"Perto da praça"}')
echo "=== REGISTER ==="
echo "$REG"
# Registration does not return a token; we'll obtain it from the login step.
# Login
LOGIN=$(curl -s -X POST "$BASE/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"luigi@example.com","senha":"senha123"}')
TOKEN=$(echo "$LOGIN" | jq -r .token)

echo "TOKEN: $TOKEN"
echo -e "\n=== LOGIN ==="
echo "$LOGIN"
# Add item
ADD=$(curl -s -X POST "$BASE/api/pedido" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"item":"Margarita","personalizacao":"extra cheese","quantidade":"2"}')
echo -e "\n=== ADD ITEM ==="
echo "$ADD"
# View cart
CART=$(curl -s -X GET "$BASE/api/carrinho" \
  -H "Authorization: Bearer $TOKEN")
echo -e "\n=== CART ==="
echo "$CART"
# Remove item (id 1)
REMOVE=$(curl -s -X POST "$BASE/api/pedido_item/delete/1" \
  -H "Authorization: Bearer $TOKEN")
echo -e "\n=== REMOVE ITEM ==="
echo "$REMOVE"
# Finalize order
FIN=$(curl -s -X POST "$BASE/api/pedido/finalizar" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"endereco_entrega":"Rua das Pizzas, 42","forma_pagamento":"credit","valor_frete":5.0,"total_pago":5.0}')
echo -e "\n=== FINALIZE ==="
echo "$FIN"
# History
HIST=$(curl -s -X GET "$BASE/api/pedidos/historico" \
  -H "Authorization: Bearer $TOKEN")
echo -e "\n=== HISTORY ==="
echo "$HIST"
