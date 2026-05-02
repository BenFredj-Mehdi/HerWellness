const dynamicLine = document.getElementById('dynamic-line');
const startBtn = document.getElementById('start-btn');
const langSelect = document.getElementById('lang');
const heroTitle = document.getElementById('hero-title');
const introText = document.getElementById('intro-text');
const startText = document.getElementById('start-text');

const content = {
  ar: {
    pageLang: 'ar',
    dir: 'rtl',
    label: 'اللغة',
    title: 'مرحبا بيك في <span>مرافق حملك الذكي</span>',
    intro: 'إرشادات مخصصة، دعم نفسي، ومساندة موثوقة في كل مرحلة من رحلتك.',
    start: 'ابدئي',
    messages: [
      'تابعي أعراضك شهر بشهر مع نصايح واضحة.',
      'بدّلي بسهولة بين العربية والإنجليزية.',
      'كمّلي رحلتك براحة، ثقة، واطمئنان.'
    ]
  },
  en: {
    pageLang: 'en',
    dir: 'ltr',
    label: 'Language',
    title: 'Welcome to <span>your smart pregnancy companion</span>',
    intro: 'Personalized guidance, emotional support, and trusted help for every stage of your journey.',
    start: 'Start',
    messages: [
      'Track symptoms month-by-month with clear advice.',
      'Switch easily between Arabic and English support.',
      'Move forward with confidence, care, and calm.'
    ]
  }
};

let currentLang = 'ar';
let messages = content[currentLang].messages;

let messageIndex = 0;
let charIndex = 0;
let deleting = false;

function resetTyping() {
  messageIndex = 0;
  charIndex = 0;
  deleting = false;
  dynamicLine.textContent = '';
}

function setLanguage(lang) {
  currentLang = lang;
  const ui = content[lang];
  messages = ui.messages;

  document.documentElement.lang = ui.pageLang;
  document.documentElement.dir = ui.dir;
  document.querySelector('.lang-label').textContent = ui.label;
  heroTitle.innerHTML = ui.title;
  introText.textContent = ui.intro;
  startText.textContent = ui.start;
  resetTyping();
}

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

langSelect.addEventListener('change', (event) => {
  setLanguage(event.target.value);
});

startBtn.addEventListener('mousemove', (event) => {
  const rect = startBtn.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  startBtn.style.background = `radial-gradient(circle at ${x}px ${y}px, #ffffff, #c9f0ff 35%, #d9c8ff 70%)`;
});

startBtn.addEventListener('mouseleave', () => {
  startBtn.style.background = 'linear-gradient(90deg, #9ee7ff, #d9c8ff)';
});

setLanguage(currentLang);
typeLoop();
