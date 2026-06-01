// api.js – login, cadastro e logout via fetch com suporte a JWT no localStorage

// ── CADASTRO ────────────────────────────────────────────────
const formCadastro = document.getElementById('cadastro');
if (formCadastro) {
  formCadastro.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = formCadastro.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Aguarde...';

    const dados = {
      nome:      document.getElementById('nome').value,
      telefone:  document.getElementById('telefone').value,
      email:     document.getElementById('email').value,
      cpf:       document.getElementById('cpf').value,
      endereco:  document.getElementById('endereco').value,
      senha:     document.getElementById('senha').value,
      referencia: document.getElementById('referencia').value,
    };

    try {
      const res  = await fetch('/api/cadastro', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(dados),
      });
      const data = await res.json();
      if (data.ok) {
        // Armazena o token se for retornado no cadastro
        if (data.token) {
          localStorage.setItem('token', data.token);
        }
        alert(data.mensagem || 'Cadastro realizado com sucesso!');
        window.location.href = '/login';
      } else {
        alert('Erro: ' + (data.erro || 'Falha no cadastro.'));
        btn.disabled = false;
        btn.textContent = 'Cadastrar';
      }
    } catch (err) {
      alert('Erro de conexão.');
      btn.disabled = false;
      btn.textContent = 'Cadastrar';
    }
  });
}

// ── LOGIN ────────────────────────────────────────────────────
const formLogin = document.getElementById('login');
if (formLogin) {
  formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = formLogin.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Aguarde...';

    const dados = {
      email: document.getElementById('email').value,
      senha: document.getElementById('senha').value,
    };

    try {
      const res  = await fetch('/api/login', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(dados),
      });
      const data = await res.json();
      if (data.ok && data.token) {
        // Armazena o token JWT no localStorage
        localStorage.setItem('token', data.token);
        window.location.href = '/';
      } else {
        alert('Erro: ' + (data.erro || 'Credenciais inválidas.'));
        btn.disabled = false;
        btn.textContent = 'Acessar';
      }
    } catch (err) {
      alert('Erro de conexão.');
      btn.disabled = false;
      btn.textContent = 'Acessar';
    }
  });
}

// ── FLUXO DE NAVEGAÇÃO DINÂMICO (JWT) ──────────────────────────
async function updateNavbar() {
  const token = localStorage.getItem('token');
  const desktopNav = document.getElementById('auth-nav-desktop');
  const mobileNav = document.getElementById('auth-nav-mobile');

  if (!token) {
    if (desktopNav) {
      desktopNav.innerHTML = `
        <button onclick="window.location.href='/login'">Login</button>
        <button onclick="window.location.href='/cadastro'">Cadastro</button>
      `;
    }
    if (mobileNav) {
      mobileNav.innerHTML = `
        <li class="nav-item"><a href="/login">Login</a></li>
        <li class="nav-item"><a href="/cadastro">Cadastro</a></li>
      `;
    }
    return;
  }

  try {
    const res = await fetch('/api/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await res.json();
    if (data.logado) {
      if (desktopNav) {
        desktopNav.innerHTML = `
          <div class="user-left">
            <a href="/meus-pedidos" class="cart-link" title="Meus pedidos">
              <i class="fa-solid fa-cart-shopping"></i>
            </a>
            <span>Olá, ${data.nome}!</span>
          </div>
          <button id="logout-btn" title="Sair" onclick="fazerLogout(event)">Sair</button>
        `;
      }
      if (mobileNav) {
        mobileNav.innerHTML = `
          <li class="nav-item"><a href="/meus-pedidos">Carrinho/Pedidos</a></li>
          <li class="nav-item"><a href="#" id="logout-btn-mobile" onclick="fazerLogout(event)">Sair (${data.nome})</a></li>
        `;
      }
    } else {
      localStorage.removeItem('token');
      updateNavbar();
    }
  } catch (err) {
    console.error("Erro ao validar sessão:", err);
  }
}

window.fazerLogout = function(e) {
  e && e.preventDefault();
  localStorage.removeItem('token');
  window.location.href = '/';
};

document.addEventListener('DOMContentLoaded', updateNavbar);
