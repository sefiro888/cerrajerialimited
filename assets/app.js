const doc = document;
const menuButton = doc.querySelector('.menu-toggle');
const mnav = doc.querySelector('#mnav');
const topbar = doc.querySelector('.top');

function setMenu(open) {
  if (!menuButton || !mnav) return;
  mnav.classList.toggle('open', open);
  mnav.setAttribute('aria-hidden', String(!open));
  topbar?.classList.toggle('menu-open', open);
  doc.body?.classList.toggle('nav-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
}
menuButton?.addEventListener('click', () => setMenu(!mnav.classList.contains('open')));
mnav?.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
doc.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (mnav?.classList.contains('open')) { setMenu(false); menuButton.focus(); }
  doc.querySelectorAll?.('.has-drop.open').forEach(d => d.classList.remove('open'));
});
window.addEventListener('resize', () => { if (window.innerWidth > 1020) setMenu(false); });

// acordeón de servicios en el menú móvil
doc.querySelector('.m-acc-btn')?.addEventListener('click', e => {
  const open = e.currentTarget.parentElement.classList.toggle('open');
  e.currentTarget.setAttribute('aria-expanded', String(open));
});

// cabecera compacta al hacer scroll
function onScroll() {
  topbar?.classList.toggle('scrolled', window.scrollY > 40);
  const h = doc.documentElement ? doc.documentElement.scrollHeight - window.innerHeight : 0;
  topbar?.style.setProperty('--p', h > 0 ? Math.min(window.scrollY / h, 1).toFixed(3) : 0);
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// aparición suave de bloques y contadores
if (typeof IntersectionObserver !== 'undefined' && doc.querySelectorAll) {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      setTimeout(() => en.target.classList.add('done'), 1100);
      en.target.querySelectorAll('[data-count]').forEach(countUp);
      io.unobserve(en.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  doc.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
  function countUp(el) {
    const end = Number(el.dataset.count);
    if (reduce || !end) return;
    const t0 = performance.now(), dur = 1300;
    (function tick(t) {
      const p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }
} else {
  doc.querySelectorAll?.('[data-reveal]').forEach(el => el.classList.add('in'));
}

// desplegable de servicios: se cierra al pulsar fuera
doc.addEventListener('click', e => {
  doc.querySelectorAll?.('.has-drop.open').forEach(d => { if (!d.contains(e.target)) d.classList.remove('open'); });
});

// foco de luz que sigue al cursor en las tarjetas
doc.querySelectorAll?.('.service-card,.veh-grid article,.why-grid article,.type-grid article,.dd>div,.steps article,.rel-grid a,.rev-card').forEach(el => {
  el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});

// selector de situación
const tabs = doc.querySelectorAll?.('.sit-tab') || [];
if (tabs.length) {
  doc.querySelector('.sit').classList.add('tabs-ready');
  doc.documentElement.classList.add('tabs-ready');
  const select = (tab, focus) => {
    tabs.forEach(t => {
      const on = t === tab;
      t.classList.toggle('active', on);
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      doc.getElementById(t.getAttribute('aria-controls')).classList.toggle('active', on);
    });
    if (focus) tab.focus();
  };
  tabs.forEach((t, i) => {
    t.tabIndex = i === 0 ? 0 : -1;
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (k) { e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true); }
    });
  });
}

// consulta guiada por WhatsApp
doc.querySelector('#quote-form')?.addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  const message = ['Hola, Cerrajería Limited. Quiero consultar un servicio.', '', 'Servicio: ' + data.get('service'), 'Vehículo: ' + data.get('car') + (data.get('year') ? ' (' + data.get('year') + ')' : ''), 'Localidad: ' + data.get('location'), data.get('message') ? 'Situación: ' + data.get('message') : ''].filter(Boolean).join('\n');
  window.location.href = 'https://wa.me/34672826060?text=' + encodeURIComponent(message);
});
