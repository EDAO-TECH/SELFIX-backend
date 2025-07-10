function toggleSeeder(action) {
    fetch('/toggle-seeder', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ action: action })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('seeder-status').innerText = `Status: ${data.status}`;
    });
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const msg = input.value;
    if (!msg.trim()) return;

    const chatBox = document.getElementById('messages');
    const userMsg = document.createElement('div');
    userMsg.classList.add('chat-msg');
    userMsg.innerHTML = `<strong>You:</strong> ${msg}`;
    chatBox.appendChild(userMsg);

    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        const reply = document.createElement('div');
        reply.classList.add('chat-msg');
        reply.innerHTML = `<strong>AI:</strong> ${data.reply}`;
        chatBox.appendChild(reply);
    });

    input.value = '';
}

// Real-time status update
function pollStatus() {
    fetch('/status')
    .then(res => res.json())
    .then(data => {
        const status = data.seeder_running ? "Seeder is ON" : "Seeder is OFF";
        document.getElementById('seeder-status').innerText = `Status: ${status}`;
    });
}
setInterval(pollStatus, 3000);
pollStatus();
