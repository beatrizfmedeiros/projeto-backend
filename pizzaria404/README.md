# 🍕 Pizzaria 404 – Guia de Instalação

## Instalação

```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

---

## Estrutura de pastas

```
pizzaria404/
├── app.py
├── requirements.txt
├── sistema.db              ← criado automaticamente na 1ª execução
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js       ← slider, scroll, menu mobile
│   │   └── api.js          ← login, cadastro, logout via fetch
│   └── image/              ← COLOQUE TODAS AS IMAGENS AQUI
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── cardapio.html
    └── sobre.html
```

---

## 📁 Imagens necessárias em static/image/

Coloque os arquivos com EXATAMENTE estes nomes:

### Ícone e fundo
| Nome do arquivo     | Onde aparece                    | Arquivo da sua pasta  |
|---------------------|---------------------------------|-----------------------|
| `icone.png`         | Logo no navbar                  | `icone.png`           |
| `favicon.ico`       | Ícone na aba do navegador       | `favicon.ico`         |
| `pizza fundo.jpeg`  | Imagem principal do Hero        | `pizza fundo.jpeg`    |

### Pizzas do cardápio (index + cardápio)
| Nome do arquivo     | Pizza                           | Arquivo da sua pasta  |
|---------------------|---------------------------------|-----------------------|
| `mussarela.jpeg`    | Pizza Mussarela                 | `mussarela.jpeg`      |
| `calabresa.jpeg`    | Pizza Calabresa                 | `calabresa.jpeg`      |
| `4queijos.jpg`      | Pizza Quatro Queijos            | `4queijos.jpg`        |

### Pizzas doces (cardápio)
| Nome do arquivo     | Pizza                           | Arquivo da sua pasta  |
|---------------------|---------------------------------|-----------------------|
| `brigadeiro.jpg`    | Pizza Brigadeiro                | `brigadeiro.jpg`      |
| `mem.jpg`           | Pizza M&M                       | `mem.jpg`             |
| `roju.jpg`          | Pizza Romeu & Julieta           | `roju.jpg`            |

### Pizzas especiais (cardápio)
| Nome do arquivo     | Pizza                           | Arquivo da sua pasta  |
|---------------------|---------------------------------|-----------------------|
| `espcoxinha.jpg`    | Pizza Coxinha                   | `espcoxinha.jpg`      |
| `espvulcao.jpg`     | Pizza Vulcão                    | `espvulcao.jpg`       |
| `espnutella.jpg`    | Pizza Nutella                   | `espnutella.jpg`      |

### Fundadores (página Sobre)
| Nome do arquivo       | Fundador       | Arquivo da sua pasta    |
|-----------------------|----------------|-------------------------|
| `fundador1.png`       | Gusteau        | `fundador1.png`         |
| `fundador2 (1).png`   | Sanji          | `fundador2 (1).png`     |
| `fundador3.png`       | Chef Hatchet   | `fundador3.png`         |

---

## ⚠️ Atenção: nomes dos arquivos

Os nomes devem ser IDÊNTICOS, incluindo maiúsculas, minúsculas e espaços.
Exemplos:
- `pizza fundo.jpeg` (com espaço)
- `fundador2 (1).png` (com espaço e parênteses)

---

## Rotas disponíveis

| Método | URL             | Descrição               |
|--------|-----------------|-------------------------|
| GET    | /               | Home                    |
| GET    | /login          | Página de login         |
| GET    | /cadastro       | Página de cadastro      |
| GET    | /cardapio       | Cardápio completo       |
| GET    | /sobre          | Sobre nós               |
| POST   | /api/login      | Autentica usuário       |
| POST   | /api/cadastro   | Cadastra usuário        |
| GET    | /api/me         | Retorna sessão ativa    |
| POST   | /api/logout     | Encerra sessão          |
