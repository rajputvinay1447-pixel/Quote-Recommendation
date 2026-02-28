const RASA_ENDPOINT = 'http://localhost:5005/webhooks/rest/webhook';
const SESSION_ID = 'user_' + Math.random().toString(36).slice(2, 10);

const chatMessages   = document.getElementById('chatMessages');
const userInput      = document.getElementById('userInput');
const sendBtn        = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const clearBtn       = document.getElementById('clearBtn');
const statusDot      = document.getElementById('statusDot');
const statusText     = document.getElementById('statusText');

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function setStatus(online) {
  if (online) {
    statusDot.className  = 'status-dot online';
    statusText.textContent = 'Connected';
  } else {
    statusDot.className  = 'status-dot offline';
    statusText.textContent = 'Offline';
  }
}

function removeWelcome() {
  const welcome = chatMessages.querySelector('.welcome-message');
  if (welcome) welcome.remove();
}

function appendMessage(text, sender, isError = false) {
  removeWelcome();

  const row = document.createElement('div');
  row.classList.add('message-row', sender);

  const avatarEl = document.createElement('div');
  avatarEl.classList.add('msg-avatar');
  avatarEl.textContent = sender === 'bot' ? 'QB' : 'You';

  const contentEl = document.createElement('div');
  contentEl.classList.add('msg-content');

  const bubble = document.createElement('div');
  bubble.classList.add('bubble');
  if (isError) bubble.classList.add('error-bubble');
  bubble.textContent = text;

  const ts = document.createElement('div');
  ts.classList.add('timestamp');
  ts.textContent = formatTime(new Date());

  contentEl.appendChild(bubble);
  contentEl.appendChild(ts);

  row.appendChild(avatarEl);
  row.appendChild(contentEl);

  chatMessages.appendChild(row);
  scrollToBottom();
}

function scrollToBottom() {
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function showTyping() {
  typingIndicator.classList.add('visible');
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
}

function hideTyping() {
  typingIndicator.classList.remove('visible');
}

async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  userInput.value = '';
  userInput.style.height = 'auto';
  sendBtn.disabled = true;

  appendMessage(trimmed, 'user');
  showTyping();

  try {
    const response = await fetch(RASA_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender: SESSION_ID, message: trimmed }),
    });

    if (!response.ok) throw new Error(`Server responded with ${response.status}`);

    const data = await response.json();
    setStatus(true);

    hideTyping();

    if (!data || data.length === 0) {
      appendMessage("I didn't get a response. Try asking for a motivation, inspiration, love, success, or funny quote!", 'bot');
      return;
    }

    for (const msg of data) {
      if (msg.text) {
        await delay(120);
        appendMessage(msg.text, 'bot');
      }
    }

  } catch (err) {
    hideTyping();
    setStatus(false);
    appendMessage('Could not reach the bot. Make sure Rasa is running at localhost:5005.', 'bot', true);
    console.error('Rasa fetch error:', err);
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

sendBtn.addEventListener('click', () => sendMessage(userInput.value));

userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage(userInput.value);
  }
});

userInput.addEventListener('input', () => {
  sendBtn.disabled = userInput.value.trim().length === 0;
  userInput.style.height = 'auto';
  userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
});

document.querySelectorAll('.category-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const msg = btn.dataset.message;
    sendMessage(msg);
  });
});

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const msg = chip.dataset.message;
    sendMessage(msg);
  });
});

clearBtn.addEventListener('click', () => {
  chatMessages.innerHTML = '';

  const welcome = document.createElement('div');
  welcome.classList.add('welcome-message');
  welcome.innerHTML = `
    <div class="welcome-icon">💬</div>
    <h2>Welcome to QuoteBot!</h2>
    <p>Ask me for quotes on motivation, inspiration, love, success, or funny topics. Use the sidebar categories or type your request below.</p>
    <div class="welcome-chips">
      <span class="chip" data-message="Hello!">Say hello</span>
      <span class="chip" data-message="Motivate me">Motivate me</span>
      <span class="chip" data-message="Make me laugh">Make me laugh</span>
    </div>
  `;
  chatMessages.appendChild(welcome);

  welcome.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => sendMessage(chip.dataset.message));
  });
});

async function checkRasaHealth() {
  try {
    const res = await fetch('http://localhost:5005/', { method: 'GET' });
    setStatus(res.ok || res.status === 404);
  } catch {
    setStatus(false);
  }
}

checkRasaHealth();
