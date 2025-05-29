async function send() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById('chat-box');
  chatBox.innerHTML += `<div><strong>나:</strong> ${message}</div>`;
  input.value = '';

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  chatBox.innerHTML += `<div><strong>GPT:</strong> ${data.response}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
