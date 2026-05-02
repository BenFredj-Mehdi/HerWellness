const dynamicLine = document.getElementById('dynamic-line');
const startBtn = document.getElementById('start-btn');

const messages = [
  'Track symptoms month-by-month with clear advice.',
  'Switch easily between Arabic and English support.',
  'Move forward with confidence, care, and calm.'
];

let messageIndex = 0;
let charIndex = 0;
let deleting = false;

function typeLoop() {
  const currentMessage = messages[messageIndex];

  if (!deleting) {
    charIndex += 1;
    dynamicLine.textContent = currentMessage.slice(0, charIndex);

    if (charIndex === currentMessage.length) {
      deleting = true;
      setTimeout(typeLoop, 1700);
      return;
    }

    setTimeout(typeLoop, 36);
    return;
  }

  charIndex -= 1;
  dynamicLine.textContent = currentMessage.slice(0, charIndex);

  if (charIndex === 0) {
    deleting = false;
    messageIndex = (messageIndex + 1) % messages.length;
  }

  setTimeout(typeLoop, deleting ? 22 : 70);
}

startBtn.addEventListener('mousemove', (event) => {
  const rect = startBtn.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  startBtn.style.background = `radial-gradient(circle at ${x}px ${y}px, #ffffff, #c9f0ff 35%, #d9c8ff 70%)`;
});

startBtn.addEventListener('mouseleave', () => {
  startBtn.style.background = 'linear-gradient(90deg, #9ee7ff, #d9c8ff)';
});

typeLoop();
