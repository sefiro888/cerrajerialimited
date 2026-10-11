const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('#main-nav');
function closeMenu() { menu.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Abrir menú'); }
menuButton?.addEventListener('click', () => {
  const isOpen = menu.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Cerrar menú' : 'Abrir menú');
});
document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu?.classList.contains('open')) { closeMenu(); menuButton.focus(); } });
document.addEventListener('click', event => { if (menu?.classList.contains('open') && !event.target.closest('.site-header')) closeMenu(); });
window.addEventListener('resize', () => { if (window.innerWidth > 1020 && menu?.classList.contains('open')) closeMenu(); });
document.querySelector('#quote-form')?.addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  const message = ['Hola, Cerrajería Limited. Quiero consultar un servicio.', '', 'Servicio: ' + data.get('service'), 'Vehículo: ' + data.get('car') + (data.get('year') ? ' (' + data.get('year') + ')' : ''), 'Localidad: ' + data.get('location'), data.get('message') ? 'Situación: ' + data.get('message') : ''].filter(Boolean).join('\n');
  window.location.href = 'https://wa.me/34672826060?text=' + encodeURIComponent(message);
});
