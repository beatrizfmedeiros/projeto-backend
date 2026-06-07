// admin.js - Gerenciamento do Painel de Admin (CRUD de produtos via API com JWT)

let allProducts = [];
let bootstrapModalInstance = null;

// Inicialização e autenticação
document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    alert("Acesso negado. Por favor, faça login.");
    window.location.href = '/login';
    return;
  }

  try {
    // Valida no backend se o usuário logado realmente possui o role admin
    const res = await fetch('/api/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();

    if (!data.logado || data.role !== 'admin') {
      alert("Acesso negado. Apenas administradores podem acessar esta página.");
      window.location.href = '/';
      return;
    }

    // Acesso permitido
    document.getElementById('admin-loading').style.display = 'none';
    document.getElementById('admin-content').classList.add('loaded');

    // Inicializa o modal do Bootstrap
    const modalEl = document.getElementById('productModal');
    bootstrapModalInstance = new bootstrap.Modal(modalEl);

    // Carrega a tabela de produtos
    await fetchProducts();

    // Registra o submit do form
    document.getElementById('productForm').addEventListener('submit', handleFormSubmit);

  } catch (err) {
    console.error("Erro na verificação de autenticação admin:", err);
    alert("Ocorreu um erro ao verificar permissões de acesso.");
    window.location.href = '/';
  }
});

// Busca os produtos
async function fetchProducts() {
  const token = localStorage.getItem('token');
  try {
    const res = await fetch('/api/admin/produtos', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    if (data.ok) {
      allProducts = data.produtos || [];
      renderProductsTable(allProducts);
    } else {
      alert("Erro ao buscar catálogo: " + (data.erro || "desconhecido"));
    }
  } catch (err) {
    console.error("Erro ao buscar produtos:", err);
    alert("Erro de conexão ao buscar catálogo.");
  }
}

// Renderiza a lista de produtos na tabela
function renderProductsTable(products) {
  const tbody = document.getElementById('produtos-table-body');
  const countSpan = document.getElementById('products-count');
  
  tbody.innerHTML = '';
  countSpan.textContent = `${products.length} Item${products.length !== 1 ? 's' : ''}`;

  if (products.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center py-5 text-muted">
          <i class="fa-solid fa-pizza-slice mb-3" style="font-size: 2rem; display: block;"></i>
          Nenhum produto cadastrado no catálogo.
        </td>
      </tr>
    `;
    return;
  }

  products.forEach(p => {
    // Formata Preço
    const precoFormatado = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(p.preco);

    // Badges de Categorias
    let catClass = 'bg-secondary';
    if (p.categoria === 'Populares') catClass = 'cat-populares';
    else if (p.categoria === 'Doces') catClass = 'cat-doces';
    else if (p.categoria === 'Especiais') catClass = 'cat-especiais';

    // Tags
    const tagsHtml = p.tags && p.tags.length > 0 
      ? p.tags.map(t => `<span class="tag-badge">${t}</span>`).join('') 
      : '<span class="text-muted small">Nenhuma</span>';

    // Status Ativo
    const statusHtml = p.ativo 
      ? `<span class="status-active"><span class="status-dot"></span> Ativo</span>`
      : `<span class="status-inactive"><span class="status-dot"></span> Inativo</span>`;

    // Botões de Ações
    const actionsHtml = `
      <div class="d-flex justify-content-end gap-2">
        <button class="btn-action-edit" onclick="openEditModal(${p.id})" title="Editar produto">
          <i class="fa-solid fa-pen-to-square"></i>
        </button>
        <button class="btn-action-delete" onclick="deleteProduct(${p.id}, '${p.nome}')" title="Excluir produto">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </div>
    `;

    // Linha da Tabela
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <img src="/static/image/${p.foto}" alt="${p.nome}" class="product-img-td" onerror="this.src='/static/image/icone.png'" />
      </td>
      <td>
        <strong class="text-light">${p.nome}</strong>
        <p class="text-muted mb-0 small text-truncate" style="max-width: 250px;" title="${p.descricao || ''}">${p.descricao || ''}</p>
      </td>
      <td>
        <span class="badge badge-category ${catClass}">${p.categoria}</span>
      </td>
      <td class="fw-semibold text-warning">
        ${precoFormatado}
      </td>
      <td>
        <div style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          ${tagsHtml}
        </div>
      </td>
      <td>
        ${statusHtml}
      </td>
      <td>
        ${actionsHtml}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Abre o Modal no modo Criação
window.openAddModal = function() {
  document.getElementById('productForm').reset();
  document.getElementById('prod-id').value = '';
  
  // Nome editável
  const nomeInput = document.getElementById('prod-nome');
  nomeInput.disabled = false;
  document.getElementById('nome-edit-warning').style.display = 'none';

  // Configura Título e Botão
  document.getElementById('productModalLabel').innerHTML = '<i class="fa-solid fa-plus me-2 text-warning"></i> Adicionar Novo Produto';
  document.getElementById('btn-save-label').textContent = 'Adicionar Produto';

  bootstrapModalInstance.show();
}

// Abre o Modal no modo Edição
window.openEditModal = function(productId) {
  const prod = allProducts.find(p => p.id === productId);
  if (!prod) return;

  document.getElementById('prod-id').value = prod.id;
  
  // Nome desativado/readonly (restrição do backend para PUT)
  const nomeInput = document.getElementById('prod-nome');
  nomeInput.value = prod.nome;
  nomeInput.disabled = true;
  document.getElementById('nome-edit-warning').style.display = 'block';

  document.getElementById('prod-preco').value = prod.preco;
  document.getElementById('prod-categoria').value = prod.categoria;
  document.getElementById('prod-foto').value = prod.foto;
  document.getElementById('prod-descricao').value = prod.descricao || '';
  document.getElementById('prod-tags').value = (prod.tags || []).join(', ');
  document.getElementById('prod-ativo').checked = !!prod.ativo;

  // Configura Título e Botão
  document.getElementById('productModalLabel').innerHTML = `<i class="fa-solid fa-pen-to-square me-2 text-warning"></i> Editar Produto: ${prod.nome}`;
  document.getElementById('btn-save-label').textContent = 'Salvar Alterações';

  bootstrapModalInstance.show();
}

// Trata o envio do formulário (Inserir ou Atualizar)
async function handleFormSubmit(e) {
  e.preventDefault();
  const token = localStorage.getItem('token');
  const submitBtn = e.target.querySelector('button[type=submit]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Enviando...';

  const id = document.getElementById('prod-id').value;
  const isEdit = !!id;

  // Monta JSON Payload
  const preco = parseFloat(document.getElementById('prod-preco').value);
  const categoria = document.getElementById('prod-categoria').value;
  const foto = document.getElementById('prod-foto').value;
  const descricao = document.getElementById('prod-descricao').value;
  const tagsText = document.getElementById('prod-tags').value;
  const ativo = document.getElementById('prod-ativo').checked;

  const tags = tagsText ? tagsText.split(',').map(t => t.trim()).filter(Boolean) : [];

  const payload = {
    preco,
    categoria,
    foto,
    descricao,
    tags,
    ativo
  };

  // Se for criação, inclui o nome (obrigatório e editável)
  if (!isEdit) {
    payload.nome = document.getElementById('prod-nome').value.trim();
  }

  const url = isEdit ? `/api/admin/produtos/${id}` : '/api/admin/produtos';
  const method = isEdit ? 'PUT' : 'POST';

  try {
    const res = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
    
    const data = await res.json();
    submitBtn.disabled = false;
    submitBtn.textContent = isEdit ? 'Salvar Alterações' : 'Adicionar Produto';

    if (data.ok) {
      bootstrapModalInstance.hide();
      await fetchProducts(); // recarrega tabela
      alert(data.mensagem || "Operação realizada com sucesso!");
    } else {
      alert("Erro ao salvar produto: " + (data.erro || "desconhecido"));
    }
  } catch (err) {
    submitBtn.disabled = false;
    submitBtn.textContent = isEdit ? 'Salvar Alterações' : 'Adicionar Produto';
    console.error("Erro ao enviar formulário do produto:", err);
    alert("Falha de conexão ao salvar produto.");
  }
}

// Exclui um produto
window.deleteProduct = async function(productId, productName) {
  if (!confirm(`Deseja realmente excluir a pizza "${productName}"? Esta ação não pode ser desfeita.`)) {
    return;
  }

  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`/api/admin/produtos/${productId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    if (data.ok) {
      await fetchProducts(); // recarrega tabela
      alert(data.mensagem || "Produto removido com sucesso.");
    } else {
      alert("Erro ao remover produto: " + (data.erro || "desconhecido"));
    }
  } catch (err) {
    console.error("Erro ao excluir produto:", err);
    alert("Falha de conexão ao remover produto.");
  }
}
