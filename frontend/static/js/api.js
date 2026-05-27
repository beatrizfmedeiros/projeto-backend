// api.js – login, cadastro e logout via fetch

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
        alert(data.mensagem);
        window.location.href = '/login';
      } else {
        alert('Erro: ' + data.erro);
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
      if (data.ok) {
        alert(data.mensagem);
        window.location.href = '/';
      } else {
        alert('Erro: ' + data.erro);
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
