// Firebase config e envio de dados do formulário de contato
    // Configuração do Firebase
    const firebaseConfig = {
      apiKey: "AIzaSyD_ok8U3gEsUaD3XcM8jml4nhXKQmPAXu4",
      authDomain: "devnotes-b2b9a.firebaseapp.com",
      projectId: "devnotes-b2b9a",
      storageBucket: "devnotes-b2b9a.firebasestorage.app",
      messagingSenderId: "614723058656",
      appId: "1:614723058656:web:3a3707290ddb3b6f628985",
      measurementId: "G-EWT4LQZ459"
    };

// Inicializa o Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('.contato-form');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const email = form.email.value;
      const telefone = form.telefone.value;
      try {
        await db.collection('contatos').add({
          email,
          telefone,
          timestamp: new Date()
        });
        alert('Contato enviado com sucesso!');
        form.reset();
      } catch (error) {
        alert('Erro ao enviar contato.');
      }
    });
  }
});
