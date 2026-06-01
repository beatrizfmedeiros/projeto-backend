// carrinho.js – Gerenciamento assíncrono do carrinho, checkout e rastreamento de pedidos via REST API

const STATUS_SEQUENCE = ["RECEBIDO", "PREPARANDO", "EM_ROTA_DE_ENTREGA", "ENTREGUE"];
let activePollingInterval = null;

// ── INICIALIZAÇÃO DA PÁGINA ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    document.getElementById('auth-warning-msg').classList.remove('d-none');
    document.getElementById('account-dashboard').classList.add('d-none');
    return;
  }
  
  document.getElementById('auth-warning-msg').classList.add('d-none');
  document.getElementById('account-dashboard').classList.remove('d-none');
  
  // Carrega os dados iniciais
  fetchCart();
  fetchHistory();
  prefillAddress();
  
  // Configuração dos eventos de Checkout
  const btnShowCheckout = document.getElementById('btn-show-checkout');
  const btnCancelCheckout = document.getElementById('btn-cancel-checkout');
  const checkoutPanel = document.getElementById('checkout-panel');
  const activeCartPanel = document.getElementById('active-cart-panel');
  const formCheckout = document.getElementById('form-checkout');
  
  if (btnShowCheckout) {
    btnShowCheckout.addEventListener('click', () => {
      checkoutPanel.classList.remove('d-none');
      // Scroll suave até o formulário
      checkoutPanel.scrollIntoView({ behavior: 'smooth' });
    });
  }
  
  if (btnCancelCheckout) {
    btnCancelCheckout.addEventListener('click', () => {
      checkoutPanel.classList.add('d-none');
      activeCartPanel.scrollIntoView({ behavior: 'smooth' });
    });
  }
  
  if (formCheckout) {
    formCheckout.addEventListener('submit', handleCheckoutSubmit);
  }
});

// ── AUXILIARES DE ESTADO DO RASTREAMENTO ──────────────────────────────
function getStepClass(currentStatus, stepName) {
  const currentIdx = STATUS_SEQUENCE.indexOf(currentStatus);
  const stepIdx = STATUS_SEQUENCE.indexOf(stepName);
  
  if (currentIdx === stepIdx) return 'active';
  if (stepIdx < currentIdx) return 'completed';
  return '';
}

function getStepperProgressStyle(currentStatus) {
  const currentIdx = STATUS_SEQUENCE.indexOf(currentStatus);
  if (currentIdx <= 0) return 'width: 0%; height: 0%;';
  const pct = (currentIdx / (STATUS_SEQUENCE.length - 1)) * 100;
  return `width: ${pct}%; height: ${pct}%;`;
}

function formatStatus(status) {
  const map = {
    'RECEBIDO': 'Pedido Recebido',
    'PREPARANDO': 'Na Cozinha / Preparando',
    'EM_ROTA_DE_ENTREGA': 'Em Rota de Entrega',
    'ENTREGUE': 'Entregue com Sucesso'
  };
  return map[status] || status;
}

// ── BUSCAR E RENDERIZAR O CARRINHO ATIVO ──────────────────────────────
async function fetchCart() {
  const token = localStorage.getItem('token');
  const container = document.getElementById('cart-items-container');
  const activeCartPanel = document.getElementById('active-cart-panel');
  
  try {
    const res = await fetch('/api/carrinho', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    
    if (data.ok) {
      activeCartPanel.classList.remove('d-none');
      
      if (data.itens && data.itens.length > 0) {
        container.innerHTML = data.itens.map(it => `
          <div class="list-group-item bg-transparent border-bottom border-secondary-subtle py-3 text-white">
            <div class="row align-items-center g-3">
              <div class="col-auto">
                ${it.foto ? 
                  `<img class="pedido-item-img" src="/static/image/${it.foto}" alt="${it.nome}" />` : 
                  `<div class="pedido-item-img bg-dark d-flex align-items-center justify-content-center text-muted" style="font-size:12px;">SEM FOTO</div>`
                }
              </div>
              <div class="col text-start">
                <h6 class="fw-bold mb-1 text-white">${it.nome}</h6>
                <p class="text-muted small mb-0">
                  Qtd: ${it.quantidade} ${it.observacao ? `• Obs: <em>${it.observacao}</em>` : ''}
                </p>
              </div>
              <div class="col-auto text-end">
                <div class="fw-bold text-warning">R$ ${it.subtotal.toFixed(2).replace('.', ',')}</div>
                <button onclick="deleteCartItem(${it.id})" class="btn btn-sm btn-outline-danger mt-2">
                  <i class="fa-regular fa-trash-can"></i> Excluir
                </button>
              </div>
            </div>
          </div>
        `).join('');
        
        // Atualiza os valores monetários
        const total = parseFloat(data.total);
        document.getElementById('cart-total-value').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
        document.getElementById('checkout-total').value = `R$ ${(total + 5.0).toFixed(2).replace('.', ',')}`;
        
        // Exibe botões de checkout
        document.getElementById('btn-show-checkout').classList.remove('d-none');
      } else {
        container.innerHTML = `
          <div class="text-center py-5 text-muted">
            <p class="mb-3"><i class="fa-solid fa-basket-shopping fs-2 text-secondary"></i></p>
            <p>Seu carrinho está vazio.</p>
            <a href="/cardapio" class="btn btn-warning fw-bold px-4 mt-2">Ir para o Cardápio</a>
          </div>
        `;
        document.getElementById('cart-total-value').textContent = 'R$ 0,00';
        document.getElementById('btn-show-checkout').classList.add('d-none');
        document.getElementById('checkout-panel').classList.add('d-none');
      }
    }
  } catch (err) {
    console.error("Erro ao buscar carrinho:", err);
  }
}

// ── REMOVER ITEM DO CARRINHO ─────────────────────────────────────────
async function deleteCartItem(itemId) {
  const token = localStorage.getItem('token');
  if (!confirm("Deseja realmente remover este item do carrinho?")) return;
  
  try {
    const res = await fetch(`/api/pedido_item/delete/${itemId}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    if (data.ok) {
      fetchCart();
    } else {
      alert("Erro ao excluir item: " + data.erro);
    }
  } catch (err) {
    alert("Erro de conexão ao remover item.");
  }
}

// ── PREENCHER ENDEREÇO SALVO AUTOMATICAMENTE ────────────────────────
async function prefillAddress() {
  const token = localStorage.getItem('token');
  try {
    const res = await fetch('/api/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    // Nota: caso o endpoint retorne os dados adicionais de cadastro, preenchemos o endereço.
    // De qualquer forma, o usuário pode digitar o endereço no campo.
  } catch (err) {
    console.log("Perfil carregado sem endereço prévio.");
  }
}

// ── FINALIZAR CHECKOUT (SUBMIT DO FORMULÁRIO) ───────────────────────
async function handleCheckoutSubmit(e) {
  e.preventDefault();
  const token = localStorage.getItem('token');
  const submitBtn = e.target.querySelector('button[type=submit]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Enviando Pedido...';
  
  const endereco = document.getElementById('checkout-endereco').value;
  const pagamento = document.getElementById('checkout-pagamento').value;
  
  // Extrai valor numérico do total a pagar
  const totalValStr = document.getElementById('checkout-total').value
    .replace('R$ ', '').replace('.', '').replace(',', '.');
  const totalPago = parseFloat(totalValStr);
  
  const dados = {
    endereco_entrega: endereco,
    forma_pagamento: pagamento,
    valor_frete: 5.0,
    total_pago: totalPago
  };
  
  try {
    const res = await fetch('/api/pedido/finalizar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(dados)
    });
    const data = await res.json();
    
    if (data.ok) {
      alert("Parabéns! Seu pedido foi finalizado com sucesso!");
      document.getElementById('checkout-panel').classList.add('d-none');
      e.target.reset();
      
      // Atualiza painéis
      fetchCart();
      fetchHistory();
    } else {
      alert("Erro ao finalizar pedido: " + data.erro);
      submitBtn.disabled = false;
      submitBtn.textContent = 'Confirmar e Finalizar Pedido';
    }
  } catch (err) {
    alert("Erro de conexão ao finalizar.");
    submitBtn.disabled = false;
    submitBtn.textContent = 'Confirmar e Finalizar Pedido';
  }
}

// ── HISTÓRICO E RASTREAMENTO REAL-TIME (POLLING) ──────────────────────
async function fetchHistory() {
  const token = localStorage.getItem('token');
  const container = document.getElementById('history-items-container');
  
  try {
    const res = await fetch('/api/pedidos/historico', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    
    if (data.ok) {
      if (data.historico && data.historico.length > 0) {
        // Renderiza a lista de pedidos no histórico
        container.innerHTML = data.historico.map(p => `
          <div class="order-history-item text-start mb-3" onclick="showOrderDetails(${p.pedido_id})">
            <div class="order-history-header text-dark">
              <span class="fw-bold text-dark"><i class="fa-solid fa-receipt text-danger me-2"></i> Pedido #${p.pedido_id}</span>
              <span class="badge ${p.status === 'ENTREGUE' ? 'bg-success' : 'bg-warning text-dark'}">${formatStatus(p.status)}</span>
            </div>
            <div class="small text-muted mb-2 mt-2">
              <strong class="text-dark">Itens:</strong> ${p.itens.map(i => `${i.nome} (x${i.quantidade})`).join(', ')}
            </div>
            <div class="d-flex justify-content-between align-items-center mt-3">
              <span class="text-muted small"><i class="fa-regular fa-calendar me-1"></i> ${p.data}</span>
              <div class="fw-bold text-danger small">
                Total Pago: R$ ${p.itens.reduce((acc, i) => acc + i.subtotal, 0).toFixed(2).replace('.', ',')}
              </div>
            </div>
          </div>
        `).join('');
        
        // Verifica se há algum pedido ATIVO (com status diferente de ENTREGUE) para rastrear
        const activeOrder = data.historico.find(p => p.status !== 'ENTREGUE');
        if (activeOrder) {
          showActiveTracking(activeOrder);
        } else {
          hideActiveTracking();
        }
      } else {
        container.innerHTML = `<div class="text-center text-muted py-4">Nenhum pedido finalizado anteriormente.</div>`;
        hideActiveTracking();
      }
    }
  } catch (err) {
    console.error("Erro ao buscar histórico:", err);
  }
}

async function showOrderDetails(pedidoId) {
  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`/api/pedido/${pedidoId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    if (data.ok) {
      // Preenche os campos do modal
      document.getElementById('detail-order-id').textContent = data.pedido_id;
      document.getElementById('detail-endereco').textContent = data.endereco_entrega || 'N/A';
      document.getElementById('detail-pagamento').textContent = data.forma_pagamento || 'N/A';
      document.getElementById('detail-frete').textContent = `R$ ${data.valor_frete.toFixed(2).replace('.', ',')}`;
      document.getElementById('detail-total').textContent = `R$ ${data.total_pago.toFixed(2).replace('.', ',')}`;
      
      const badge = document.getElementById('detail-status');
      badge.textContent = formatStatus(data.status);
      badge.className = `badge ${data.status === 'ENTREGUE' ? 'bg-success' : 'bg-warning text-dark'}`;
      
      document.getElementById('detail-data').textContent = data.data;
      
      // Renderiza os itens na tabela
      const tbody = document.getElementById('detail-items-body');
      tbody.innerHTML = data.itens.map(it => `
        <tr class="align-middle text-dark">
          <td>
            <div class="d-flex align-items-center gap-2">
              ${it.foto ? 
                `<img class="pedido-item-img" style="width: 40px; height: 30px; object-fit: cover;" src="/static/image/${it.foto}" alt="${it.nome}" />` : 
                `<div class="pedido-item-img bg-light d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 30px; font-size: 8px;">SEM FOTO</div>`
              }
              <span>${it.nome}</span>
            </div>
          </td>
          <td>${it.quantidade}</td>
          <td class="text-muted small">${it.observacao || '-'}</td>
          <td class="text-end">R$ ${it.valor_unitario.toFixed(2).replace('.', ',')}</td>
          <td class="text-end text-danger fw-bold">R$ ${it.subtotal.toFixed(2).replace('.', ',')}</td>
        </tr>
      `).join('');
      
      // Exibe o modal usando o Bootstrap 5 nativo
      const modalEl = document.getElementById('pedidoDetalhesModal');
      const bsModal = new bootstrap.Modal(modalEl);
      bsModal.show();
    } else {
      alert("Erro ao buscar detalhes: " + data.erro);
    }
  } catch (err) {
    alert("Erro de conexão ao carregar detalhes.");
  }
}
window.showOrderDetails = showOrderDetails;

// Injeta e inicializa o widget de rastreamento visual ativo
function showActiveTracking(pedido) {
  const panel = document.getElementById('active-tracking-panel');
  panel.classList.remove('d-none');
  
  panel.innerHTML = `
    <div class="tracking-container mb-4 text-start">
      <div class="tracking-header text-white">
        <h6 class="fw-bold mb-0">
          <i class="fa-solid fa-pizza-slice text-warning animate-bounce"></i> Acompanhando Pedido #${pedido.pedido_id}
        </h6>
        <span class="order-status-badge" id="tracking-status-badge">${formatStatus(pedido.status)}</span>
      </div>
      
      <div class="tracking-stepper mt-4">
        <div class="tracking-progress-fill" id="tracking-progress-line" style="${getStepperProgressStyle(pedido.status)}"></div>
        
        <div class="step-node ${getStepClass(pedido.status, 'RECEBIDO')}" id="step-node-recebido">
          <div class="step-circle"><i class="fa-solid fa-receipt"></i></div>
          <div class="step-label">Recebido</div>
        </div>
        <div class="step-node ${getStepClass(pedido.status, 'PREPARANDO')}" id="step-node-preparando">
          <div class="step-circle"><i class="fa-solid fa-fire-burner"></i></div>
          <div class="step-label">Preparando</div>
        </div>
        <div class="step-node ${getStepClass(pedido.status, 'EM_ROTA_DE_ENTREGA')}" id="step-node-rota">
          <div class="step-circle"><i class="fa-solid fa-motorcycle"></i></div>
          <div class="step-label">Em Rota</div>
        </div>
        <div class="step-node ${getStepClass(pedido.status, 'ENTREGUE')}" id="step-node-entregue">
          <div class="step-circle"><i class="fa-solid fa-house-chimney-user"></i></div>
          <div class="step-label">Entregue</div>
        </div>
      </div>
    </div>
  `;
  
  // Inicia o loop de Polling se já não estiver rodando
  if (!activePollingInterval) {
    activePollingInterval = setInterval(() => pollOrderStatus(pedido.pedido_id), 5000);
  }
}

function hideActiveTracking() {
  document.getElementById('active-tracking-panel').classList.add('d-none');
  if (activePollingInterval) {
    clearInterval(activePollingInterval);
    activePollingInterval = null;
  }
}

// Função de Polling: Consulta o status individual de 5 em 5 segundos
async function pollOrderStatus(pedidoId) {
  const token = localStorage.getItem('token');
  try {
    const res = await fetch(`/api/pedido/${pedidoId}/status`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    
    if (res.status === 200 && data.status) {
      const status = data.status;
      
      // Atualiza o crachá de texto e a linha de progresso
      const badge = document.getElementById('tracking-status-badge');
      if (badge) badge.textContent = formatStatus(status);
      
      const progressLine = document.getElementById('tracking-progress-line');
      if (progressLine) progressLine.style = getStepperProgressStyle(status);
      
      // Atualiza as classes dos nós
      const nodes = {
        'RECEBIDO': document.getElementById('step-node-recebido'),
        'PREPARANDO': document.getElementById('step-node-preparando'),
        'EM_ROTA_DE_ENTREGA': document.getElementById('step-node-rota'),
        'ENTREGUE': document.getElementById('step-node-entregue')
      };
      
      for (const [stepName, element] of Object.entries(nodes)) {
        if (element) {
          element.className = `step-node ${getStepClass(status, stepName)}`;
        }
      }
      
      // Se chegou em ENTREGUE, encerra o polling e atualiza o histórico final
      if (status === 'ENTREGUE') {
        clearInterval(activePollingInterval);
        activePollingInterval = null;
        setTimeout(() => {
          alert(` Oba! Seu pedido #${pedidoId} foi entregue! Aproveite a sua pizza! 🍕`);
          fetchHistory();
        }, 1500);
      }
    }
  } catch (err) {
    console.error("Erro durante o polling de status:", err);
  }
}
