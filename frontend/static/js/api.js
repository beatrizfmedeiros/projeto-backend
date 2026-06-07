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
          <a href="/meus-pedidos" class="nav-link-icon animate-fade" data-tooltip="Carrinho & Pedidos" style="margin-right: 15px;">
            <i class="fa-solid fa-cart-shopping"></i>
          </a>
          <div class="user-dropdown-container">
            <button class="user-dropdown-btn nav-link-icon" id="user-menu-btn" data-tooltip="Minha Conta">
              <i class="fa-solid fa-user"></i>
            </button>
            <div class="user-dropdown-menu" id="user-dropdown-menu">
              <div class="user-dropdown-header">Olá, ${data.nome}!</div>
              ${data.role === 'admin' ? '<a href="/admin" class="user-dropdown-item"><i class="fa-solid fa-gear"></i> Painel Admin</a>' : ''}
              <a href="/meus-pedidos" class="user-dropdown-item"><i class="fa-solid fa-clock-rotate-left"></i> Meus Pedidos</a>
              <div class="user-dropdown-divider"></div>
              <a href="#" class="user-dropdown-item text-danger" onclick="fazerLogout(event)"><i class="fa-solid fa-right-from-bracket"></i> Sair</a>
            </div>
          </div>
        `;
      }
      if (mobileNav) {
        mobileNav.innerHTML = `
          ${data.role === 'admin' ? '<li class="nav-item"><a href="/admin"><i class="fa-solid fa-gear me-2"></i> Painel Admin</a></li>' : ''}
          <li class="nav-item"><a href="/meus-pedidos"><i class="fa-solid fa-cart-shopping me-2"></i> Carrinho/Pedidos</a></li>
          <li class="nav-item"><a href="#" id="logout-btn-mobile" onclick="fazerLogout(event)"><i class="fa-solid fa-right-from-bracket me-2"></i> Sair (${data.nome})</a></li>
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

// Gerenciamento dinâmico do clique fora para fechar o menu dropdown
document.addEventListener('click', (e) => {
  const btn = e.target.closest('#user-menu-btn');
  const menu = document.getElementById('user-dropdown-menu');
  
  if (btn) {
    e.stopPropagation();
    menu.classList.toggle('show');
  } else if (menu && !e.target.closest('#user-dropdown-menu')) {
    menu.classList.remove('show');
  }
});

document.addEventListener('DOMContentLoaded', updateNavbar);
