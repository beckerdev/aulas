// Script para rastrear e registrar todas as ações do usuário no site no Firestore
// Requer Firebase já inicializado no projeto

// Função para obter IP do usuário (usando serviço externo)
async function getUserIP() {
  try {
    const res = await fetch('https://api.ipify.org?format=json');
    const data = await res.json();
    return data.ip;
  } catch {
    return 'IP_desconhecido';
  }
}

// Função para gerar ou obter identificador único do usuário (localStorage)
function getOrCreateUserId() {
  let userId = localStorage.getItem('devnotes_user_id');
  if (!userId) {
    userId = 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    localStorage.setItem('devnotes_user_id', userId);
  }
  return userId;
}

// Função para registrar evento no Firestore
async function logUserEvent(eventType, details) {
  const userId = getOrCreateUserId();
  const ip = await getUserIP();
  await db.collection('user_events').add({
    userId,
    ip,
    eventType,
    details,
    url: window.location.pathname,
    timestamp: new Date()
  });
}

// Registrar navegação entre páginas
window.addEventListener('DOMContentLoaded', () => {
  logUserEvent('page_view', { title: document.title });
});

// Registrar cliques em links e botões
['click', 'submit'].forEach(evt => {
  document.addEventListener(evt, function(e) {
    let target = e.target;
    if (target.tagName === 'A' || target.tagName === 'BUTTON' || evt === 'submit') {
      logUserEvent(evt, {
        tag: target.tagName,
        text: target.innerText || target.value || '',
        id: target.id || '',
        class: target.className || ''
      });
    }
  }, true);
});

// Registrar rolagem (scroll)
let lastScroll = 0;
window.addEventListener('scroll', function() {
  const now = Date.now();
  if (now - lastScroll > 2000) { // registra a cada 2s
    logUserEvent('scroll', { scrollY: window.scrollY });
    lastScroll = now;
  }
});
