// script.js – slider, scroll, menu mobile, barra de progresso

// ── BARRA DE PROGRESSO ──────────────────────────────────────
window.addEventListener('scroll', () => {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  const total = document.documentElement.scrollHeight - window.innerHeight;
  const pct   = total > 0 ? (window.scrollY / total) * 100 : 0;
  bar.style.width = pct + '%';
});

// ── MENU MOBILE ─────────────────────────────────────────────
const mobileBtn  = document.getElementById('mobile_btn');
const mobileMenu = document.getElementById('mobile_menu');
if (mobileBtn && mobileMenu) {
  mobileBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
  });
}

// ── SCROLL SUAVE ────────────────────────────────────────────
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

// Links de âncora do navbar
document.querySelectorAll('a[href^="/#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const href = link.getAttribute('href');
    if (window.location.pathname === '/') {
      e.preventDefault();
      const id = href.replace('/#', '');
      scrollToSection(id);
      if (mobileMenu) mobileMenu.classList.remove('active');
    }
  });
});

// ── ANIMAÇÃO DE SCROLL DAS SEÇÕES ───────────────────────────
const sections = document.querySelectorAll('.section');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

sections.forEach(s => observer.observe(s));

// ── SLIDER DE DEPOIMENTOS ────────────────────────────────────
let currentSlide = 0;

function showSlide(n) {
  const slides = document.querySelectorAll('.slide');
  if (!slides.length) return;
  slides.forEach(s => s.classList.remove('active'));
  currentSlide = (n + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
}

function nextSlide() { showSlide(currentSlide + 1); }
function prevSlide() { showSlide(currentSlide - 1); }

// Auto-play
setInterval(() => {
  if (document.querySelector('.slide')) nextSlide();
}, 5000);

// ── ACTIVE NAV ITEM NO SCROLL ────────────────────────────────
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY + 120;
  document.querySelectorAll('.nav-item').forEach(item => {
    const link = item.querySelector('a');
    if (!link) return;
    const href = link.getAttribute('href');
    if (!href) return;
    const id = href.replace('/#', '').replace('#', '');
    const el = document.getElementById(id);
    if (el) {
      if (el.offsetTop <= scrollY && el.offsetTop + el.offsetHeight > scrollY) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    }
  });
});

// ── FORMULÁRIO DE CONTATO ────────────────────────────────────
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Mensagem enviada! Entraremos em contato em breve.');
    contactForm.reset();
  });
}
