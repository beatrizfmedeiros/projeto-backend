# 🍕 Pizzaria 404 – Guia de Instalação e Execução

O projeto **Pizzaria 404** foi reorganizado para garantir uma separação limpa de responsabilidades entre o **Backend** (código em Python com Flask e banco de dados SQLite) e o **Frontend** (páginas HTML do Jinja2, CSS, JS e imagens).

---

## 📁 Nova Estrutura de Pastas

```
/
├── backend/
│   ├── app.py                 ← Servidor Flask e APIs
│   ├── requirements.txt       ← Dependências do Python
│   └── sistema.db             ← Banco de dados (criado na 1ª execução)
├── frontend/
│   ├── static/                ← Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   ├── image/
│   │   └── js/
│   └── templates/             ← Páginas e templates HTML do Flask/Jinja2
├── Makefile                   ← Comandos de automação (Linux/macOS)
├── iniciar (1).bat            ← Script legado de inicialização (Windows)
└── README.md                  ← Este guia
```

---

## 🚀 Como Executar

### No Linux / macOS (Recomendado)

Usamos o **Makefile** para simplificar a execução:

1. **Instalar Dependências**:
   ```bash
   make install
   ```

2. **Iniciar o Servidor**:
   ```bash
   make run
   ```

Acesse o sistema em: http://localhost:5000

---

### No Windows (Legado)

Dê um duplo clique no arquivo `iniciar (1).bat` na raiz do repositório. Ele instalará as dependências silenciosamente e abrirá a página no seu navegador.

---

## 📁 Imagens necessárias em frontend/static/image/

Coloque os arquivos de imagens com os seguintes nomes exatamente dentro da pasta `frontend/static/image/`:

### Ícone e fundo
- `icone.png` (Logo no navbar)
- `favicon.ico` (Ícone na aba do navegador)
- `pizza fundo.jpeg` (Imagem principal do Hero)

### Pizzas do cardápio (index + cardápio)
- `mussarela.jpeg`
- `calabresa.jpeg`
- `4queijos.jpg`

### Pizzas doces (cardápio)
- `brigadeiro.jpg`
- `mem.jpg`
- `roju.jpg`

### Pizzas especiais (cardápio)
- `espcoxinha.jpg`
- `espvulcao.jpg`
- `espnutella.jpg`

### Fundadores (página Sobre)
- `fundador1.png`
- `fundador2 (1).png`
- `fundador3.png`
