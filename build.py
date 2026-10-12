from pathlib import Path
from urllib.parse import quote
import json
from PIL import Image

ROOT = Path(__file__).parent
D = ROOT / 'dist'
A = D / 'assets'
A.mkdir(parents=True, exist_ok=True)
Image.open(ROOT.parent / 'Logo para paleta de colores.jpeg').save(A / 'identidad.webp', quality=92)


# ---------- imagen para compartir (WhatsApp, redes) ----------
from PIL import ImageDraw, ImageFont, ImageFilter
SITE = 'https://sefiro888.github.io/cerrajerialimited/'


def make_og():
    W, H = 1200, 630
    bgname = 'hero-home' if (A / 'hero-home.webp').exists() else 'hero'
    bg = Image.open(A / (bgname + '.webp')).convert('RGB')
    r = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * r), round(bg.height * r)), Image.LANCZOS)
    bg = bg.crop((bg.width - W, (bg.height - H) // 2, bg.width, (bg.height - H) // 2 + H))
    shade = Image.new('RGBA', (W, H))
    px = shade.load()
    for x in range(W):
        a = int(250 - 190 * min(x / (W * .85), 1))
        for y in range(H):
            px[x, y] = (9, 9, 11, a)
    bg = Image.alpha_composite(bg.convert('RGBA'), shade)
    d = ImageDraw.Draw(bg)
    logo = Image.open(A / 'identidad.webp').convert('RGB').resize((200, 200), Image.LANCZOS)
    mask = Image.new('L', (200, 200), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 199, 199), fill=255)
    bg.paste(logo, (70, 70), mask)
    d.ellipse((68, 68, 272, 272), outline=(255, 255, 255, 70), width=2)
    f = str(A / 'barlow-condensed.ttf')
    d.text((70, 305), 'CERRAJERÍA', font=ImageFont.truetype(f, 112), fill=(255, 255, 255))
    d.text((70, 405), 'LIMITED', font=ImageFont.truetype(f, 112), fill=(229, 34, 47))
    d.rectangle((70, 540, 130, 544), fill=(229, 34, 47))
    d.text((70, 556), 'URGENCIAS 24 H · GUADALAJARA Y MADRID · 672 826 060', font=ImageFont.truetype(f, 30), fill=(230, 230, 235))
    bg.convert('RGB').save(A / 'og-image.jpg', quality=84, optimize=True)


make_og()

PHONE = '672826060'
PHONE_FMT = '672 826 060'
TEL = 'tel:+34' + PHONE
WA = 'https://wa.me/34' + PHONE
EMAIL = 'cerrajerialimited@gmail.com'
IG = 'https://www.instagram.com/cerrajerialimited/'
FB = 'https://www.facebook.com/profile.php?id=61585461347179'
PA = 'https://www.paginasamarillas.es/f/cerrajero-de-coches-24h-copias-de-llaves-cerrajeria-limited_310766514_000000001.html'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Calle+Zaragoza+53+Guadalajara'


def wa(text):
    return WA + '?text=' + quote(text)


def img(name, fallback):
    """Usa la imagen nueva si existe en assets; si no, la que ya había."""
    return name if (A / (name + '.webp')).exists() else fallback


# ---------- iconos ----------
ICONS = {
    'key': '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    'copy': '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    'car': '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><path d="M12 15.5v2"/>',
    'chip': '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
    'van': '<path d="M3 17V8a1 1 0 0 1 1-1h10v10"/><path d="M14 10h3.2a1 1 0 0 1 .8.4l3 3.6c.3.3.4.6.4 1V17h-1.4"/><path d="M14 17h-3.2M5 17H3"/><circle cx="8" cy="17.5" r="2"/><circle cx="18" cy="17.5" r="2"/><path d="M7 7v4M17 10v3h3"/>',
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'wa': 'FILL<path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.8 11.8 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.9 0-3.17-1.24-6.16-3.48-8.41Z"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'bolt': '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    'pin': '<path d="M20 10c0 5-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    'card': '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20M6 15h4"/>',
    'home': '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .71-1.53l7-6a2 2 0 0 1 2.58 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    'moto': '<circle cx="5" cy="16" r="3"/><circle cx="19" cy="16" r="3"/><path d="M7.5 14h5l4-4h-10.5m1.5 4 4-4"/><path d="M13 6h2l1.5 3 2 4"/>',
    'truck': '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    'bus': '<path d="M8 6v6M15 6v6M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><path d="M9 18h5"/><circle cx="16" cy="18" r="2"/>',
    'tool': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'x': '<path d="M18 6 6 18M6 6l12 12"/>',
    'arrow': '<path d="M5 12h14m-7-7 7 7-7 7"/>',
    'star': '<path d="M11.53 2.3a.53.53 0 0 1 .95 0l2.31 4.68a2.12 2.12 0 0 0 1.6 1.16l5.16.75a.53.53 0 0 1 .3.9l-3.74 3.64a2.12 2.12 0 0 0-.61 1.88l.88 5.14a.53.53 0 0 1-.77.56l-4.62-2.43a2.12 2.12 0 0 0-1.97 0L6.4 21.01a.53.53 0 0 1-.77-.56l.88-5.14a2.12 2.12 0 0 0-.61-1.88L2.16 9.8a.53.53 0 0 1 .3-.9l5.16-.75a2.12 2.12 0 0 0 1.6-1.16z"/>',
}


def icon(name, cls=''):
    body = ICONS[name]
    if body.startswith('FILL'):
        return '<svg class="ic %s" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">%s</svg>' % (cls, body[4:])
    return ('<svg class="ic %s" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (cls, body))


# ---------- componentes ----------
def btn(text='Pedir presupuesto', href='contacto.html', kind='', ic='arrow'):
    return '<a class="button %s" href="%s">%s<span class="b-ic">%s</span></a>' % (kind, href, text, icon(ic))


def heading(kicker, h, intro='', center=False):
    lead = '<p class="lead">%s</p>' % intro if intro else ''
    return '<div class="section-heading%s" data-reveal><p class="eyebrow">%s</p><h2>%s</h2>%s</div>' % (
        ' center' if center else '', kicker, h, lead)


def sec(inner, cls='', sid=''):
    return '<section class="section %s"%s>%s</section>' % (cls, ' id="%s"' % sid if sid else '', inner)


def checks(items):
    return '<ul class="check-list" data-reveal>' + ''.join('<li>%s</li>' % x for x in items) + '</ul>'


def steps(items, cols=''):
    return '<div class="steps %s">' % cols + ''.join(
        '<article data-reveal><span class="step-num">0%d</span><h3>%s</h3><p>%s</p></article>' % (i + 1, h, p)
        for i, (h, p) in enumerate(items)) + '</div>'


def faq(items):
    return '<div class="faq" data-reveal>' + ''.join(
        '<details><summary>%s<span aria-hidden="true">+</span></summary><p>%s</p></details>' % (q, a)
        for q, a in items) + '</div>'


def faq_section(kicker, h, items):
    return sec('<div>' + heading(kicker, h, 'Lo que más nos preguntan antes de llamar. Si tu duda no está aquí, escríbenos por WhatsApp.') + '</div>' + faq(items), 'faq-section')


POS = {'taller-movil': ' style="object-position:25% center"', 'apertura-coche': ' style="object-position:40% center"', 'van-guadalajara': ' style="object-position:60% center"'}


def split(kicker, h, paras, image='keys', items=None, reverse=False, cta=None, label='CERRAJERÍA LIMITED / AUTOMOCIÓN', dark=False):
    body = ''.join('<p data-reveal>%s</p>' % p for p in paras)
    cta = cta or btn()
    return sec(
        '<div class="photo-wrap" data-reveal><img src="assets/%s.webp" loading="lazy" alt="Imagen ilustrativa de cerrajería de automoción"%s>'
        '<span class="photo-label">%s</span></div><div>%s%s%s<div data-reveal>%s</div></div>'
        % (image, POS.get(image, ''), label, heading(kicker, h), body, checks(items) if items else '', cta),
        'split%s%s' % (' reverse' if reverse else '', ' dark-section' if dark else ''))


def cards3(items):
    return '<div class="type-grid">' + ''.join(
        '<article data-reveal><span>%s</span><h3>%s</h3><p>%s</p>%s</article>' % (a, b, c, d)
        for a, b, c, d in items) + '</div>'


def dosdonts(do, dont):
    return ('<div class="dd"><div data-reveal class="dd-do"><h3>%s Sí, mejor así</h3><ul>%s</ul></div>'
            '<div data-reveal class="dd-dont"><h3>%s Mejor evita</h3><ul>%s</ul></div></div>') % (
        icon('check'), ''.join('<li>%s</li>' % x for x in do),
        icon('x'), ''.join('<li>%s</li>' % x for x in dont))


BRANDS = ['Mercedes-Benz', 'BMW', 'Audi', 'Volkswagen', 'SEAT', 'Škoda', 'Porsche', 'Toyota', 'Honda', 'Nissan',
          'Peugeot', 'Dacia', 'Renault', 'Citroën', 'Ford', 'Opel', 'Fiat', 'Hyundai', 'Kia', 'Suzuki', 'Mazda',
          'Mitsubishi', 'Jeep', 'Volvo', 'Land Rover', 'Jaguar', 'Lexus', 'Subaru', 'Chevrolet', 'Tesla', 'Smart',
          'Mini', 'Alfa Romeo', 'Cadillac', 'Iveco', 'Saab', 'Daewoo']


def brand_marquee():
    row = ''.join('<span>%s</span>' % b for b in BRANDS)
    return ('<section class="brand-marquee" aria-label="Marcas con las que trabajamos"><p class="bm-title">TRABAJAMOS CON TODAS LAS MARCAS Y MODELOS<em> · Y MUCHAS MÁS</em></p>'
            '<div class="marquee" aria-hidden="true"><div class="marquee-track">%s%s</div></div></section>' % (row, row))


def brand_grid():
    return ('<div class="brand-list" data-reveal>' + ''.join('<span>%s</span>' % b for b in BRANDS[:24]) + '<span class="more">Y muchas más…</span></div>'
            '<p class="small-note">Marcas citadas como referencia de consulta. La viabilidad depende del modelo, el año y el sistema de seguridad concretos.</p>')


VEHICLES = [('car', 'Coches', 'Turismos de cualquier marca, con llave mecánica, mando o tarjeta.'),
            ('moto', 'Motos', 'Llaves y mandos de motocicleta, con o sin inmovilizador.'),
            ('van', 'Furgonetas', 'Vehículos de trabajo y reparto: que no pare tu actividad.'),
            ('truck', 'Camiones', 'Asistencia para vehículos pesados. Consulta modelo y ubicación.'),
            ('bus', 'Autobuses', 'Llaves y cerraduras de vehículos de transporte de viajeros.')]


def vehicles():
    return ('<div class="veh-grid">' + ''.join(
        '<article data-reveal><span class="veh-ic">%s</span><h3>%s</h3><p>%s</p></article>' % (icon(i), t, p) for i, t, p in VEHICLES) + '</div>')


SERVICES = [
    ('01', 'Pérdida total de llaves', 'Fabricamos y programamos una llave nueva aunque no conserves ninguna. Sin grúa y sin esperar días.', 'perdida-de-llaves.html', 'key'),
    ('02', 'Copias y programación', 'Llaves simples, con mando o tarjeta. Corte, chip y programación adaptados a tu vehículo.', 'copia-de-llaves.html', 'copy'),
    ('03', 'Apertura de vehículos', 'Si las llaves se han quedado dentro, abrimos con técnica adaptada y orientada a no dañar el coche.', 'apertura-de-vehiculos.html', 'car'),
    ('04', 'Cerraduras y clausor', 'Reparación de bombines y cerraduras de coche. Primero localizamos la avería, después te contamos opciones.', 'servicios.html#cerraduras', 'lock'),
    ('05', 'Electrónica de automoción', 'Centralitas, cuadros, inmovilizadores y alarmas. Diagnóstico y viabilidad según el vehículo.', 'servicios.html#electronica', 'chip'),
    ('06', 'Taller móvil 24 h', 'Vamos donde estés, a domicilio y sin coste adicional de desplazamiento. Todos los días del año.', 'cobertura.html', 'van'),
]


def service_cards(n=6):
    return '<div class="service-grid">' + ''.join(
        '<a class="service-card" href="%s" data-reveal><div class="card-top">%s<span>%s</span></div><h3>%s</h3><p>%s</p>'
        '<span class="text-link">Ver servicio <b>%s</b></span></a>' % (s[3], icon(s[4]), s[0], s[1], s[2], icon('arrow'))
        for s in SERVICES[:n]) + '</div>'


def related(skip):
    pool = [('perdida-de-llaves.html', 'Pérdida total de llaves', 'key'), ('copia-de-llaves.html', 'Copias y programación', 'copy'),
            ('apertura-de-vehiculos.html', 'Apertura de vehículos', 'car'), ('cobertura.html', 'Cobertura y taller móvil', 'van'),
            ('servicios.html', 'Todos los servicios', 'tool')]
    return sec(heading('SEGUIR EXPLORANDO', 'También puede<br>interesarte.') + '<div class="rel-grid">' + ''.join(
        '<a href="%s" data-reveal>%s<span>%s</span>%s</a>' % (u, icon(i), t, icon('arrow')) for u, t, i in pool if u != skip)
        + '</div>', 'related')


def why():
    items = [('bolt', 'Rápidos', 'Llegamos en poco tiempo. Cuéntanos dónde estás y confirmamos la disponibilidad.'),
             ('shield', 'Seguros', 'Trabajamos sin dañar tu vehículo y verificamos la autorización antes de intervenir.'),
             ('star', 'Garantizados', 'Calidad y garantía en cada servicio, con llaves originales y compatibles.'),
             ('home', 'A domicilio', 'Taller móvil: vamos a tu casa, tu trabajo o tu aparcamiento, sin coste adicional.'),
             ('clock', '24 h, 365 días', 'Atención de urgencias todos los días del año, también noches y festivos.'),
             ('card', 'Presupuesto previo', 'Sabes qué se hace y cuánto cuesta antes de empezar. Pago con tarjeta.')]
    return '<div class="why-grid">' + ''.join(
        '<article data-reveal>%s<h3>%s</h3><p>%s</p></article>' % (icon(i), t, p) for i, t, p in items) + '</div>'


def coverage_art(note='ASISTENCIA MÓVIL / 24 H'):
    svg = ('<svg class="map-svg" viewBox="0 0 640 460" aria-hidden="true">'
           '<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>'
           '<radialGradient id="gl" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#e5222f" stop-opacity=".38"/><stop offset="1" stop-color="#e5222f" stop-opacity="0"/></radialGradient></defs>'
           '<rect width="640" height="460" fill="url(#g)"/>'
           '<g fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="1.4"><path d="M-10 90C150 120 300 60 650 110"/><path d="M60 470C140 360 90 260 200 170S330 20 360-10"/><path d="M650 330C520 300 470 380 330 400S100 430 -10 400"/><circle cx="240" cy="310" r="44"/></g>'
           '<circle cx="440" cy="150" r="130" fill="url(#gl)"/>'
           '<circle cx="440" cy="150" r="82" fill="#e5222f" fill-opacity=".1" stroke="#e5222f" stroke-opacity=".7" stroke-width="1.5"/>'
           '<circle cx="240" cy="310" r="104" fill="none" stroke="#ffc21a" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="5 7"/>'
           '<path class="route-line" d="M240 310C300 282 370 214 440 150" fill="none" stroke="#ff3d49" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="3 9"/>'
           '<circle class="pulse" cx="440" cy="150" r="9" fill="#e5222f"/><circle cx="440" cy="150" r="8" fill="#e5222f" stroke="#fff" stroke-width="2.5"/>'
           '<circle class="pulse p2" cx="240" cy="310" r="9" fill="#ffc21a"/><circle cx="240" cy="310" r="8" fill="#ffc21a" stroke="#fff" stroke-width="2.5"/></svg>')
    return ('<div class="area-art" data-reveal>' + svg +
            '<div class="pin-label g"><b>GUADALAJARA</b><small>Base · servicio 24 h</small></div>'
            '<div class="pin-label m"><b>MADRID</b><small>Comunidad · previa consulta</small></div>'
            '<div class="map-legend"><span><i class="lg1"></i>Zona principal</span><span><i class="lg2"></i>Previa consulta</span></div>'
            '<span class="area-note">%s</span></div>' % note)


# ---------- home: selector de situación ----------
SITUATIONS = [
    ('Perdí todas las llaves', 'key', 'Pérdida total de llaves',
     'Aunque no tengas ninguna llave, fabricamos y programamos una nueva para tu vehículo. Nada de grúa ni de esperar días.',
     ['Fabricación y programación en el acto', 'Llaves originales y compatibles', 'Taller móvil: vamos donde estés'],
     'perdida-de-llaves.html', 'Hola, he perdido todas las llaves de mi coche. ¿Podéis ayudarme?'),
    ('Llaves dentro del coche', 'car', 'Apertura sin daños',
     'Si el coche se ha cerrado con las llaves dentro, no fuerces la puerta. Abrimos con una técnica adaptada a tu vehículo.',
     ['Técnica orientada a no dañar el coche', 'Atención las 24 horas', 'Verificamos autorización antes de abrir'],
     'apertura-de-vehiculos.html', 'Hola, me he quedado con las llaves dentro del coche. ¿Podéis abrirlo?'),
    ('Quiero una copia', 'copy', 'Copia y programación',
     'Una segunda llave hoy es una urgencia que te ahorras mañana. Llaves simples, con mando y tarjetas, para coches, motos y furgonetas.',
     ['Corte según el perfil de tu cerradura', 'Programación del chip y del mando', 'Prueba de todas las funciones'],
     'copia-de-llaves.html', 'Hola, quiero hacer una copia de la llave de mi vehículo. ¿Me orientáis?'),
    ('Mando o cerradura fallan', 'lock', 'Cerraduras y electrónica',
     'La llave no gira, el mando no responde o el coche no reconoce el chip. Localizamos la avería antes de proponerte una solución.',
     ['Reparación de bombines y cerraduras', 'Inmovilizadores, centralitas y cuadros', 'Diagnóstico previo y presupuesto claro'],
     'servicios.html', 'Hola, mi llave o cerradura no funciona bien. ¿Podéis revisarlo?'),
]


def situations():
    tabs = ''.join('<button type="button" role="tab" class="sit-tab%s" id="tab%d" aria-controls="panel%d" aria-selected="%s">%s<span>%s</span></button>'
                   % (' active' if i == 0 else '', i, i, 'true' if i == 0 else 'false', icon(s[1]), s[0]) for i, s in enumerate(SITUATIONS))
    panels = ''.join(
        '<div class="sit-panel%s" role="tabpanel" id="panel%d" aria-labelledby="tab%d"><div><p class="eyebrow">LA SOLUCIÓN</p><h3>%s</h3><p>%s</p>%s'
        '<div class="sit-actions">%s%s</div></div><div class="sit-side"><span class="sit-n">0%d</span><a class="sit-link" href="%s">Más información %s</a></div></div>'
        % (' active' if i == 0 else '', i, i, s[2], s[3], checks(s[4]),
           btn('Llamar ahora', TEL, '', 'phone'), btn('Contar mi caso', wa(s[6]), 'secondary', 'wa'), i + 1, s[5], icon('arrow'))
        for i, s in enumerate(SITUATIONS))
    return sec(heading('ELIGE TU SITUACIÓN', 'Cuéntanos qué ha pasado.<br>Te decimos cómo <em>resolverlo.</em>', 'Cuatro situaciones habituales, cuatro caminos claros. Elige la tuya y contacta con un solo toque.')
               + '<div class="sit" data-reveal><div class="sit-tabs" role="tablist" aria-label="Situación">%s</div><div class="sit-panels">%s</div></div>' % (tabs, panels),
               'sit-section', 'situacion')


def trust_strip():
    items = [('24', 'h', 'Atención de urgencias'), ('365', '', 'Días del año, también festivos'),
             ('0', '€', 'Coste adicional por ir a tu domicilio'), ('5', '', 'Tipos de vehículo: coche, moto, furgoneta, camión y bus')]
    return ('<section class="proof-strip">' + ''.join(
        '<div data-reveal><b><i data-count="%s">%s</i><span>%s</span></b><p>%s</p></div>' % (n, n, u, t) for n, u, t in items) + '</section>')


REVIEWS = [
    ('Silvia G.', 'Excelentes profesionales. Se desplazaron a mí domicilio para hacerme copia de llave Renault Megane. Rapidez y calidad en el trabajo y muy amables. Precio ajustado', 'Copia de llave a domicilio'),
    ('Sergio', 'Todo perfecto perdi las llaves y me atendieron muy bien. Me hicieron 2 llaves 1 normal y 1 otra con mando con cierre centralizado. Lo recomiendo.', 'Pérdida total de llaves'),
    ('Angel Luis A.', 'Muy buenos profesionales y buena gente, me atendieron súper rápido y hasta que no dejaron todo funcionando correctamente no pararon. Muy recomendable', 'Atención rápida'),
    ('Fernando M.', 'Jonathan hizo un trabajo impecable. Además fue muy amable y claro en todo el proceso y nos solucionó el problema de las llaves del coche en el día.', 'Copia de llaves'),
    ('Daniel C.', 'Muy agradable, el trato y los consejos han sido genial y excelente servicio, me atendió Miguel muy contento con su servicio y ayuda, excelente', 'Apertura de automóvil'),
]
GMAPS = 'https://www.google.com/maps/search/?api=1&query=Cerrajer%C3%ADa+Limited+Guadalajara+Calle+Zaragoza+53'


def stars(n=5):
    return '<span class="stars" role="img" aria-label="%d estrellas">%s</span>' % (n, icon('star') * n)


def reviews():
    cards = ''.join(
        '<article class="rev-card" data-reveal>%s<blockquote>%s</blockquote><footer><span class="rev-av">%s</span><div><b>%s</b><small>%s · Reseña en Google</small></div></footer></article>' % (stars(), t, n[0], n, tag)
        for n, t, tag in REVIEWS)
    cards += '<a class="rev-card rev-more" data-reveal href="%s" target="_blank" rel="noopener"><p class="eyebrow">TODAS LAS OPINIONES</p><h3>Léelas tú mismo en Google</h3><span class="text-link">Ver en Google Maps <b>%s</b></span></a>' % (GMAPS, icon('arrow'))
    summary = ('<div class="rev-sum" data-reveal><p class="eyebrow">OPINIONES REALES DE CLIENTES</p><div class="rev-score"><b>4,8</b>%s</div><p>Valoración media en Google con <strong>38 opiniones</strong>. Estas son algunas de ellas, tal como las escribieron.</p>%s</div>'
               % (stars(), btn('Escríbenos', WA, 'secondary', 'wa')))
    return sec('<div class="rev-wrap">' + summary + '<div class="rev-grid">' + cards + '</div></div>', 'dark-section reviews')


# ---------- cuerpos de página ----------
home = brand_marquee() + trust_strip() + situations()
home += sec(heading('TODO LO QUE TU VEHÍCULO NECESITA', 'Un taller completo.<br>Un solo teléfono.', 'Llaves, mandos, cerraduras y electrónica de automoción, con un taller móvil que va donde tú estés.') + service_cards() + '<div class="section-tail" data-reveal>' + btn('Ver todos los servicios', 'servicios.html', 'secondary') + '</div>', 'dark-section')
home += split('TALLER MÓVIL · SIN GRÚA', 'La solución<br>llega a ti.', [
    'Cuando el coche no abre o no arranca, lo último que quieres es moverlo. Nuestro taller móvil acude a tu domicilio, tu trabajo o tu aparcamiento, <strong>sin coste adicional por el desplazamiento</strong>.',
    'Fabricamos y programamos llaves en el acto, con llaves originales y compatibles, para que vuelvas a arrancar sin esperas.'],
    image=img('van-guadalajara', 'mobile'), items=['Sin grúa y sin esperar días', 'Fabricación y programación en el acto', 'Servicio 24 horas, 365 días al año'], cta=btn('Pedir asistencia', wa('Hola, necesito asistencia de cerrajería de coche en mi ubicación.'), '', 'wa'))
home += sec(heading('PARA CUALQUIER VEHÍCULO', 'Coches, motos,<br>furgonetas y más.', 'No solo turismos: atendemos todo tipo de vehículos, de particulares y de empresas.') + vehicles(), '')
home += sec(heading('ASÍ DE FÁCIL', 'Del problema<br>a la solución.') + steps([
    ('Llama o escribe', 'Dinos qué ha pasado, dónde estás y la marca, modelo y año de tu vehículo.'),
    ('Presupuesto previo', 'Te explicamos qué hay que hacer y cuánto cuesta antes de empezar. Sin sorpresas.'),
    ('Vamos a ti', 'Nuestro taller móvil acude a tu ubicación. Tú no tienes que moverte.'),
    ('Vuelves a arrancar', 'Probamos contigo apertura, cierre y arranque. Servicio con garantía.')], 'four'), 'dark-section')
home += sec(heading('POR QUÉ CERRAJERÍA LIMITED', 'Compromisos que<br>se notan.', 'Lo que buscas cuando tienes un problema con tu coche: rapidez, seguridad y claridad.', ) + why())
home += reviews()
home += sec('<div>' + heading('GUADALAJARA · COMUNIDAD DE MADRID', 'Vamos donde<br>nos necesitas.', 'En casa, en un aparcamiento o allí donde se haya quedado tu vehículo. Consulta la disponibilidad del servicio móvil para tu ubicación.') + checks(['Guadalajara y alrededores', 'Comunidad de Madrid, previa consulta', 'Atención de urgencias todos los días']) + '<div data-reveal>' + btn('Consultar cobertura', 'cobertura.html', 'secondary') + '</div></div>' + coverage_art(), 'coverage-preview')
home += faq_section('RESPUESTAS PARA DECIDIR', 'Antes de<br>llamarnos.', [
    ('¿Podéis hacer una llave si he perdido todas?', 'Sí. Fabricamos y programamos una llave nueva aunque no conserves ninguna. La viabilidad concreta depende de la marca, el modelo, el año y el sistema del vehículo; con esos datos te confirmamos el caso.'),
    ('¿Cuánto cuesta el servicio?', 'Depende de la llave, de la programación y de la situación del vehículo. Te damos un presupuesto personalizado antes de intervenir. Aceptamos pago con tarjeta.'),
    ('¿Atendéis por la noche y en festivos?', 'Sí. La atención de urgencias es de 24 horas, los 365 días del año. Llama o escribe y confirmamos disponibilidad para tu ubicación.'),
    ('¿Hay que llevar el coche a algún sitio?', 'No. Somos un taller móvil: vamos a tu domicilio sin coste adicional, evitando grúa y esperas.'),
    ('¿Trabajáis con mi marca?', 'Trabajamos con todas las marcas y modelos más habituales y con muchas más. Mándanos marca, modelo y año por WhatsApp y te lo confirmamos.'),
    ('¿Dañaréis mi coche al abrirlo?', 'Nuestra técnica de apertura está orientada a no dañar el vehículo. Antes de intervenir, valoramos el sistema de cierre y la técnica adecuada.')])

svc = sec(heading('ESPECIALISTAS EN AUTOMOCIÓN', 'Cada problema,<br>su solución.', 'La cerrajería de vehículos combina precisión mecánica y electrónica. Por eso identificamos el origen del problema antes de proponer nada.') + service_cards())
svc += sec('<div>' + heading('TIPOS DE LLAVE', 'Reconoce<br>tu llave.', 'El tipo de llave define el trabajo y el presupuesto. Estas son las tres familias más habituales.') + '</div>' + cards3([
    ('01 / MECÁNICA', 'Llaves simples', 'Una llave metálica o con cabeza de plástico, a veces con un transponder para el arranque.', ''),
    ('02 / ACCESO Y ARRANQUE', 'Llaves con mando', 'Con botones de apertura y cierre, plegables o fijas. Requieren corte, chip y programación del mando.', ''),
    ('03 / SISTEMAS ESPECÍFICOS', 'Tarjetas y llaves inteligentes', 'Cada sistema tiene sus requisitos. Consulta compatibilidad y presupuesto para tu modelo.', '')]), 'dark-section')
svc += sec('<div>' + heading('MECÁNICA · CERRADURAS Y CLAUSOR', 'Cuando la llave<br>deja de girar.') + '</div><div><p data-reveal>Una llave que se atasca, una cerradura que no responde o un clausor que dificulta el arranque requieren una revisión específica. Forzar el mecanismo puede empeorar el problema y encarecer la reparación.</p><p data-reveal>Reparamos bombines y cerraduras de coche. Valoramos el estado del conjunto y te explicamos las alternativas según el vehículo y la avería.</p>' + checks(['Problemas de giro y desgaste', 'Revisión del bombín y del mecanismo', 'Comprobación de cierre y funcionamiento']) + '</div>', 'feature-row', 'cerraduras')
svc += split('ELECTRÓNICA DE AUTOMOCIÓN', 'Más allá<br>de la llave.', [
    'El mando abre las puertas, pero el vehículo puede necesitar reconocer un chip para permitir el arranque. Los fallos mecánicos y electrónicos no siempre tienen la misma solución.',
    'Ofrecemos servicios relacionados con centralitas, cuadros, inmovilizadores y alarmas. Cuéntanos los síntomas y los datos del vehículo para valorar el diagnóstico y la viabilidad del trabajo.'],
    image=img('tecnico-programando', 'keys'), reverse=True, items=['Programación de centralitas y cuadros', 'Instalación de inmovilizadores y alarmas', 'Programación de llaves con chip'])
svc = svc.replace('class="section split reverse"', 'class="section split reverse" id="electronica"', 1)
svc += sec(heading('PARA CUALQUIER VEHÍCULO', 'Coches, motos,<br>furgonetas y más.') + vehicles() + '<div class="spacer"></div>' + brand_grid(), 'dark-section')
svc += sec('<div>' + heading('INFORMACIÓN ÚTIL', 'Prepara estos<br>cuatro datos.', 'Con esta información podemos darte un presupuesto y una orientación mucho más rápidos.') + '</div><div>' + steps([
    ('Tu vehículo', 'Marca, modelo y año de fabricación.'), ('La llave', 'Tipo de llave, mando o tarjeta; si conservas alguna copia.'),
    ('El problema', 'Qué funciona, qué ha dejado de funcionar y desde cuándo.'), ('La ubicación', 'Localidad y lugar donde se encuentra el vehículo.')]) + '</div>', 'feature-row')
svc += reviews()
svc += faq_section('SERVICIOS', 'Dudas sobre<br>los servicios.', [
    ('¿Qué servicios ofrecéis?', 'Pérdida total de llaves, copia y programación, apertura de vehículos, reparación de cerraduras y bombines, y electrónica de automoción: centralitas, cuadros, inmovilizadores y alarmas.'),
    ('¿Trabajáis con vehículos que no son coches?', 'Sí. Atendemos coches, motos, furgonetas, camiones y autobuses. Consulta el modelo concreto para confirmar la viabilidad.'),
    ('¿Puedo pagar con tarjeta?', 'Sí, aceptamos pago con tarjeta (Visa y Mastercard, entre otras). Confirma el método al pedir tu presupuesto.')])

loss = split('PÉRDIDA TOTAL / NUEVA LLAVE', 'Sin ninguna llave.<br>Con una solución.', [
    'Perder todas las llaves no significa que debas dar tu coche por perdido. En Cerrajería Limited <strong>fabricamos y programamos nuevas llaves</strong> para tu vehículo, aunque no tengas ninguna.',
    'El procedimiento depende del sistema de seguridad y del modelo. Antes de desplazarnos, revisamos la información del vehículo y confirmamos qué intervención es posible.'],
    image=img('taller-movil', 'mobile'), items=['Fabricación de una nueva llave', 'Programación según el sistema del vehículo', 'Comprobación de acceso y arranque', 'Sin grúa y sin esperar días'])
loss += sec(heading('QUÉ SUCEDE DESPUÉS DE TU LLAMADA', 'Del bloqueo<br>a volver a arrancar.') + steps([
    ('Identificamos el vehículo', 'Necesitamos marca, modelo, año y ubicación. Indica también si la llave se perdió o fue sustraída.'),
    ('Verificamos la autorización', 'Ten preparada tu identificación y la documentación que acredite tu relación con el vehículo.'),
    ('Preparamos una nueva llave', 'Valoramos fabricación y programación según el sistema. Disponibilidad y tiempos se confirman para cada caso.'),
    ('Comprobamos el resultado', 'Revisamos apertura, cierre y arranque, según las funciones de la llave y la intervención realizada.')], 'four'), 'dark-section')
loss += sec('<div>' + heading('CONSEJO PRÁCTICO', 'Lo primero:<br>no fuerces nada.') + '</div>' + dosdonts(
    ['Localiza el vehículo y reúne marca, modelo y año', 'Ten a mano tu documentación e identificación', 'Llama o escribe y cuéntanos tu ubicación', 'Si sospechas un robo de llaves, díselo al técnico'],
    ['Introducir herramientas en la puerta o la cerradura', 'Forzar el marco o el bombín', 'Dejar el coche abierto si sospechas un robo', 'Mover el vehículo si no es necesario']), 'feature-row')
loss += sec(heading('SE ADAPTA A TU VEHÍCULO', 'Tu coche, tu moto,<br>tu furgoneta.') + vehicles() + '<div class="spacer"></div>' + brand_grid(), 'dark-section')
loss += reviews()
loss += faq_section('PÉRDIDA TOTAL', 'Resolvemos<br>tus dudas.', [
    ('¿Necesito tener la llave original?', 'No es necesario conservar ninguna llave. Fabricamos y programamos una nueva; la viabilidad concreta se confirma para tu vehículo.'),
    ('¿Es necesario llevar el coche a un taller?', 'No. Contamos con taller móvil: acudimos a la ubicación del vehículo, sin grúa. Si tu caso requiere algo adicional, te lo decimos antes.'),
    ('¿Cuánto tardáis en llegar o terminar?', 'Depende de la ubicación, la disponibilidad y el sistema del vehículo. Al contactar te orientamos sobre tu caso, sin prometer un único tiempo para todos los servicios.'),
    ('¿Qué documentación debo preparar?', 'Tu identificación y la documentación del vehículo o autorización correspondiente. El técnico te indicará lo necesario para verificar el servicio.'),
    ('¿Y si me han robado las llaves?', 'Coméntalo al contactar. Se pueden valorar medidas apropiadas para el sistema de tu vehículo, además de fabricar una nueva llave.')])

copies = sec('<div>' + heading('LA LLAVE QUE NECESITA TU VEHÍCULO', 'No es solo copiar.<br>Es hacerla funcionar.', 'El corte permite accionar la cerradura. En muchos vehículos, el chip y el mando también necesitan una adaptación electrónica. Revisamos qué requiere tu llave.') + '</div>' + cards3([
    ('01 / MECÁNICA', 'Llave simple', 'La parte metálica se adapta al perfil de la cerradura. Según el vehículo, puede incorporar un transponder para el arranque.', ''),
    ('02 / ACCESO Y ARRANQUE', 'Llave con mando', 'Integra botones de apertura y cierre. La copia puede requerir corte, programación del chip y adaptación del mando.', ''),
    ('03 / SISTEMAS ESPECÍFICOS', 'Tarjeta y llave inteligente', 'Cada sistema tiene sus requisitos. Consulta compatibilidad, disponibilidad y presupuesto para el modelo concreto.', '')]))
copies += split('UN REPUESTO, MUCHA TRANQUILIDAD', 'Haz la copia<br>antes de necesitarla.', [
    'Si conservas una llave operativa, es el mejor momento para hacer una segunda. Indícanos si abre, cierra y arranca correctamente: esos datos ayudan a definir el trabajo.',
    'Una carcasa deteriorada, botones que fallan o un vehículo que no reconoce la llave pueden necesitar reparación o diagnóstico, además de una copia. Te explicamos qué opción tiene sentido.'],
    image=img('llave-copia', 'keys'), items=['Corte de la llave según perfil', 'Programación cuando sea necesaria', 'Prueba de las funciones disponibles'])
copies += sec(heading('4 RAZONES PARA HACERLA YA', 'Una segunda llave<br>es un seguro.') + '<div class="why-grid four">' + ''.join(
    '<article data-reveal>%s<h3>%s</h3><p>%s</p></article>' % (icon(i), t, p) for i, t, p in [
        ('clock', 'Evita la urgencia', 'Con una copia de repuesto, perder una llave es un contratiempo, no una emergencia.'),
        ('card', 'Cuesta menos', 'Copiar con una llave operativa suele ser más sencillo que fabricar desde cero.'),
        ('shield', 'Más seguridad', 'Una llave de repuesto bien guardada te protege ante pérdidas o robos.'),
        ('home', 'A domicilio', 'Acudimos donde estés, sin coste adicional de desplazamiento.')]) + '</div>', 'dark-section')
copies += sec(heading('COMPATIBILIDAD', 'Tu marca es el comienzo.<br>El modelo es la clave.', 'Consulta para turismos, furgonetas, motos y otros vehículos. La marca por sí sola no garantiza la compatibilidad: también importan el año y el sistema de seguridad.') + brand_grid())
copies += reviews()
copies += faq_section('COPIAS Y MANDOS', 'Una segunda llave,<br>sin dudas.', [
    ('¿Una copia de la parte metálica basta para arrancar?', 'No siempre. Si el vehículo utiliza inmovilizador electrónico, puede necesitar un chip compatible y su programación, además del corte.'),
    ('¿Podéis revisar un mando que no funciona?', 'Consulta con la marca, modelo y síntomas. La batería, la carcasa, los botones o la electrónica pueden requerir distintas soluciones.'),
    ('¿Las llaves inteligentes tienen el mismo precio?', 'No. Sus componentes y procesos son diferentes. El presupuesto especifica el tipo de llave y las operaciones incluidas.'),
    ('¿Puedo pedir una copia a domicilio?', 'Sí, vamos a tu ubicación sin coste adicional de desplazamiento. Confirmamos antes qué trabajo puede hacerse allí.')])

opening = split('APERTURA PROFESIONAL', 'La llave dentro.<br>La calma contigo.', [
    'Cerrar el coche con las llaves dentro ocurre en un instante. La prioridad es recuperar el acceso con técnicas apropiadas para el vehículo y <strong>orientadas a no dañarlo</strong>.',
    'Explica dónde está el coche, su marca, modelo y año, y si la llave está dentro o la cerradura no responde. Con esa información valoramos el tipo de asistencia.'],
    image=img('apertura-coche', 'hero'), items=['Atención para llaves dentro del vehículo', 'Técnica adaptada al sistema de cierre', 'Verificación de autorización antes de abrir', 'Atención 24 horas, 365 días'])
opening += sec('<div>' + heading('DIFERENTES SITUACIONES, DISTINTAS SOLUCIONES', '¿Qué te ha<br>ocurrido?') + '</div>' + cards3([
    ('ACCESO', 'Llaves dentro', 'Solicita apertura y avisa si las llaves están en el habitáculo o en el maletero. No intentes forzar el marco.', ''),
    ('CIERRE', 'La cerradura falla', 'Describe si la llave gira, se atasca o no entra. Puede ser necesario revisar el bombín además de abrir el vehículo.', ''),
    ('LLAVE', 'No encuentras ninguna', 'Una apertura recupera el acceso, pero no sustituye a la llave de arranque. Consulta pérdida total.', '<a class="text-link" href="perdida-de-llaves.html">Ver pérdida total <b>%s</b></a>' % icon('arrow'))]), 'dark-section')
opening += sec('<div>' + heading('MIENTRAS LLEGAMOS', 'Qué hacer<br>y qué no.') + '<p class="notice" data-reveal>Si hay una persona o un animal en peligro dentro del vehículo, llama primero al 112.</p></div>' + dosdonts(
    ['Indica tu ubicación exacta y si estás en un garaje', 'Ten a mano marca, modelo y año del coche', 'Prepara tu identificación y documentación', 'Mantente en un lugar seguro y visible'],
    ['Forzar la puerta con herramientas', 'Usar objetos para alcanzar el pomo o la manilla', 'Golpear cristales o marcos', 'Dar vueltas con el coche buscando una solución']), 'feature-row')
opening += sec(heading('SEGUIMOS CONTIGO', 'Del acceso a<br>la llave nueva.', 'Si además necesitas una llave, resolvemos las dos cosas en la misma visita.') + '<div class="rel-grid">' + ''.join(
    '<a href="%s" data-reveal>%s<span>%s</span>%s</a>' % (u, icon(i), t, icon('arrow')) for u, t, i in [('perdida-de-llaves.html', 'Pérdida total de llaves', 'key'), ('copia-de-llaves.html', 'Copia de llaves', 'copy')]) + '</div>')
opening += faq_section('APERTURAS', 'Antes de<br>recuperar el acceso.', [
    ('¿La apertura incluye una llave nueva?', 'Son intervenciones distintas. Si has perdido todas las llaves, indícalo para valorar también la fabricación y programación de una nueva.'),
    ('¿Podéis abrir cualquier coche?', 'El procedimiento depende del modelo y del sistema de cierre. Te pedimos los datos para confirmar la asistencia.'),
    ('¿El coche sufrirá daños?', 'El servicio está orientado a abrir sin dañar el vehículo. El técnico valora la situación y la técnica adecuada antes de intervenir.'),
    ('¿Atendéis de noche?', 'Sí, las 24 horas del día, los 365 días del año.')])

coverage = sec('<div>' + heading('DOS ÁREAS, UN MISMO SERVICIO', 'Guadalajara<br>y Madrid.', 'Cerrajería Limited atiende en Guadalajara y la Comunidad de Madrid. Confirma por teléfono la cobertura y disponibilidad para la ubicación exacta de tu vehículo.') + checks(['Guadalajara y alrededores', 'Comunidad de Madrid, previa consulta', 'Taller móvil según servicio y vehículo', 'Sin coste adicional por ir a tu domicilio']) + '<div data-reveal>' + btn('Confirmar mi ubicación', wa('Hola, quiero consultar asistencia en mi ubicación.'), '', 'wa') + '</div></div>' + coverage_art('REPRESENTACIÓN ILUSTRATIVA DE LAS ÁREAS'), 'coverage-preview')
coverage += split('EL TALLER SE MUEVE', 'Tu vehículo<br>marca el destino.', [
    'El taller móvil permite resolver intervenciones junto al vehículo. Es especialmente útil cuando no puedes acceder al coche o no tienes llave para arrancarlo.',
    'Dinos si está en la vía pública, en casa o en un aparcamiento. El acceso al lugar, el tipo de trabajo y la disponibilidad condicionan la asistencia. Lo confirmamos contigo.'],
    image=img('van-guadalajara', 'mobile'), reverse=True, items=['Sin grúa y sin esperar días', 'Atención de urgencias 24 h', 'A domicilio sin coste adicional'])
coverage += sec(heading('ANTES DEL DESPLAZAMIENTO', 'Todo claro desde<br>la primera llamada.') + steps([
    ('Zona y acceso', 'Confirma localidad, ubicación y condiciones de entrada al aparcamiento o recinto.'),
    ('Intervención necesaria', 'Explica si necesitas abrir, copiar, programar o resolver una pérdida total.'),
    ('Presupuesto y disponibilidad', 'Consulta coste y horario estimado antes de aceptar el servicio.')]), 'dark-section')
coverage += sec('<div>' + heading('REFERENCIA DE CONTACTO', 'También puedes<br>localizarnos.') + '<p data-reveal>Calle Zaragoza 53<br>19005 Guadalajara</p><p data-reveal>Para visitas, confirma previamente la atención y el servicio por teléfono.</p><div data-reveal>' + btn('Ver ubicación en Maps', MAPS, 'secondary', 'pin') + '</div></div><div class="location-detail" data-reveal><b>24 h</b><p>Atención de urgencias<br>Lunes a domingo</p><a href="%s">%s</a></div>' % (TEL, PHONE_FMT), 'location-panel')
coverage += faq_section('COBERTURA', 'Sobre la zona<br>de servicio.', [
    ('¿Cubrís mi localidad?', 'Atendemos en Guadalajara y alrededores y, previa consulta, en la Comunidad de Madrid. Escríbenos tu ubicación y lo confirmamos.'),
    ('¿Cobráis el desplazamiento?', 'El servicio a domicilio se anuncia sin coste adicional. Confirma las condiciones al pedir tu presupuesto.'),
    ('¿Podéis ir a un garaje o aparcamiento?', 'Sí, indícanos el acceso y las condiciones del recinto para valorar la intervención.')])

contact = sec('<div>' + heading('ELIGE CÓMO HABLAMOS', 'Una llamada.<br>El primer paso.') +
              '<a class="contact-channel" data-reveal href="%s"><small>TELÉFONO / URGENCIAS 24 H</small><strong>%s <span>%s</span></strong></a>' % (TEL, PHONE_FMT, icon('phone')) +
              '<a class="contact-channel" data-reveal href="%s"><small>WHATSAPP / DATOS Y CONSULTAS</small><strong>Cuéntanos tu caso <span>%s</span></strong></a>' % (WA, icon('wa')) +
              '<a class="contact-channel email" data-reveal href="mailto:%s"><small>CORREO ELECTRÓNICO</small><strong>%s</strong></a>' % (EMAIL, EMAIL) +
              '<p class="contact-address" data-reveal>Calle Zaragoza 53 · 19005 Guadalajara<br>Confirma por teléfono la atención antes de visitar.</p>'
              '<div class="social-links" data-reveal><a href="%s" target="_blank" rel="noopener">Instagram ↗</a><a href="%s" target="_blank" rel="noopener">Facebook ↗</a><a href="%s" target="_blank" rel="noopener">Páginas Amarillas ↗</a></div></div>' % (IG, FB, PA) +
              '<div class="form-panel" data-reveal><p class="eyebrow">CONSULTA GUIADA</p><h3>Preparar mi consulta</h3><p>Completa los datos para abrir WhatsApp con tu mensaje preparado. Tú decides cuándo enviarlo.</p>'
              '<form id="quote-form"><label>¿Qué necesitas?<select name="service" required><option value="">Selecciona un servicio</option><option>Pérdida total de llaves</option><option>Copia o programación de llaves</option><option>Apertura de vehículo</option><option>Cerraduras o clausor</option><option>Electrónica de automoción</option><option>Otra consulta</option></select></label>'
              '<div class="form-row"><label>Marca y modelo<input name="car" placeholder="Ej.: SEAT León" required maxlength="100" autocomplete="off"></label><label>Año<input name="year" type="number" min="1960" max="2027" placeholder="Ej.: 2019"></label></div>'
              '<label>Localidad<input name="location" placeholder="¿Dónde está el vehículo?" required maxlength="150" autocomplete="address-level2"></label>'
              '<label>Cuéntanos qué ha ocurrido<textarea name="message" rows="4" maxlength="1500" placeholder="¿Conservas alguna llave? ¿El coche está cerrado?"></textarea></label>'
              '<button class="button" type="submit">Preparar mensaje en WhatsApp <span class="b-ic">%s</span></button><p class="form-note">Estos datos no se guardan en la web. Al continuar se abrirá WhatsApp, donde podrás revisar el mensaje antes de enviarlo.</p><p id="form-status" role="status"></p></form></div>' % icon('wa'), 'contact-layout')
contact += sec(heading('INFORMACIÓN PRÁCTICA', 'Todo lo que<br>conviene saber.') + '<div class="why-grid">' + ''.join(
    '<article data-reveal>%s<h3>%s</h3><p>%s</p></article>' % (icon(i), t, p) for i, t, p in [
        ('clock', 'Horario', 'Atención de urgencias 24 horas, de lunes a domingo, los 365 días del año.'),
        ('card', 'Formas de pago', 'Aceptamos pago con tarjeta (Visa y Mastercard, entre otras). Confirma el método al pedir presupuesto.'),
        ('pin', 'Zona', 'Guadalajara y alrededores, y Comunidad de Madrid previa consulta.')]) + '</div>', 'dark-section')
contact += reviews()
contact += sec(heading('PARA AYUDARTE MEJOR', 'Ten estos datos<br>a mano.') + steps([
    ('Vehículo', 'Marca, modelo, año y tipo de llave.'), ('Situación', 'Si conservas alguna llave y qué funciones fallan.'), ('Lugar', 'Localidad, ubicación y acceso al vehículo.')]))

pages = {
    'index.html': dict(title='Cerrajería de coches 24 h en Guadalajara y Madrid', kicker='CERRAJERÍA DE AUTOMOCIÓN · 24 HORAS', heading='Vuelve a tener<br>el <em>control.</em>', intro='Llaves perdidas, un coche cerrado o un mando que no responde. Taller móvil 24 horas en Guadalajara y Madrid: vamos donde estés.', img=img('hero-home', 'hero'), body=home),
    'servicios.html': dict(title='Servicios de cerrajería de automoción', kicker='LLAVES · CERRADURAS · ELECTRÓNICA', heading='Precisión en<br>cada <em>solución.</em>', intro='Apertura, fabricación y programación de llaves, reparación de cerraduras y electrónica de automoción. Un servicio pensado alrededor de tu vehículo.', img=img('hero-servicios', 'keys'), body=svc),
    'perdida-de-llaves.html': dict(title='Pérdida total de llaves de coche', kicker='PÉRDIDA TOTAL DE LLAVES · TALLER MÓVIL', heading='Sin llaves.<br>Sin <em>quedarte atrás.</em>', intro='Aunque no conserves ninguna copia, fabricamos y programamos una nueva llave. Cuéntanos qué vehículo tienes y dónde estás.', img=img('hero-perdida', 'mobile'), body=loss),
    'copia-de-llaves.html': dict(title='Copias y programación de llaves de coche', kicker='COPIAS · MANDOS · TRANSPONDERS', heading='Una copia.<br>Más <em>tranquilidad.</em>', intro='Llaves simples, mandos y sistemas electrónicos: una copia adaptada a tu vehículo para no depender de una única llave.', img=img('hero-copia', 'keys'), body=copies),
    'apertura-de-vehiculos.html': dict(title='Apertura de coches y vehículos 24 horas', kicker='APERTURA DE VEHÍCULOS · ATENCIÓN 24 H', heading='Recupera<br>el <em>acceso.</em>', intro='¿Las llaves se han quedado dentro del coche? Apertura profesional, con una técnica adaptada a tu vehículo y orientada a no dañarlo.', img=img('hero-apertura', 'hero'), body=opening),
    'cobertura.html': dict(title='Taller móvil en Guadalajara y Madrid', kicker='GUADALAJARA · COMUNIDAD DE MADRID', heading='Tu imprevisto.<br>Nuestro <em>destino.</em>', intro='Un taller móvil que acerca la solución a tu vehículo. Dinos tu ubicación y confirmamos cobertura, disponibilidad y el trabajo que necesitas.', img=img('hero-cobertura', 'mobile'), body=coverage),
    'contacto.html': dict(title='Contacto y presupuesto de cerrajería de coches', kicker='HABLEMOS DE TU VEHÍCULO', heading='El camino<br>empieza <em>aquí.</em>', intro='Llama para una urgencia o prepara tu consulta por WhatsApp. Con los datos del vehículo y tu ubicación podremos orientarte mejor.', img=img('hero-contacto', 'keys'), body=contact),
}

NAV = [('index.html', 'Inicio'), ('servicios.html', 'Servicios'), ('cobertura.html', 'Cobertura'), ('contacto.html', 'Contacto')]
SUB = [('perdida-de-llaves.html', 'Pérdida total de llaves', 'key', 'Nueva llave aunque no tengas ninguna'),
       ('copia-de-llaves.html', 'Copias de llaves', 'copy', 'Llaves simples, mandos y tarjetas'),
       ('apertura-de-vehiculos.html', 'Apertura de vehículos', 'car', 'Sin daños, 24 horas'),
       ('servicios.html#cerraduras', 'Cerraduras y clausor', 'lock', 'Bombines y cerraduras de coche'),
       ('servicios.html#electronica', 'Electrónica', 'chip', 'Centralitas, cuadros e inmovilizadores')]
SERVICE_PAGES = {s[0].split('#')[0] for s in SUB} | {'servicios.html'}
TICKER = ['ATENCIÓN 24 HORAS · 365 DÍAS', 'TALLER MÓVIL: VAMOS A DONDE ESTÉS', 'A DOMICILIO SIN COSTE ADICIONAL', 'APERTURA DE VEHÍCULOS SIN DAÑOS',
          'FABRICAMOS TU LLAVE EN EL ACTO', 'SIN GRÚA Y SIN ESPERAR DÍAS', 'TODAS LAS MARCAS Y MODELOS', 'PAGO CON TARJETA']


def ticker():
    row = ''.join('<span>%s</span>' % t for t in TICKER)
    return ('<div class="ticker" role="region" aria-label="Información del servicio"><div class="ticker-track">%s%s</div></div>' % (row, row.replace('<span>', '<span aria-hidden="true">')))


def header(current):
    cur = lambda u: ' aria-current="page"' if u == current or (u == 'servicios.html' and current in SERVICE_PAGES) else ''
    links = ''
    for u, l in NAV:
        if u == 'servicios.html':
            drop = ''.join('<a href="%s"><span class="dm-ic">%s</span><span><b>%s</b><small>%s</small></span>%s</a>' % (su, icon(si), sl, sd, icon('arrow')) for su, sl, si, sd in SUB)
            promo = ('<div class="dm-promo"><p class="eyebrow"><span class="live"></span>URGENCIAS 24 H</p><h4>¿Te has quedado<br>sin llaves?</h4><p>Taller móvil: vamos donde estés, sin coste adicional de desplazamiento.</p>'
                     '<a class="button" href="' + TEL + '">' + PHONE_FMT + '<span class="b-ic">' + icon('phone') + '</span></a><a class="dm-wa" href="' + WA + '">' + icon('wa') + 'Escribir por WhatsApp</a></div>')
            links += ('<div class="has-drop"><a href="%s"%s aria-haspopup="true">%s<svg class="caret" viewBox="0 0 10 6" aria-hidden="true"><path d="m1 1 4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></a>'
                      '<div class="drop"><div class="dm-list"><p class="dm-title">NUESTROS SERVICIOS</p>%s<a class="dm-all" href="servicios.html">Ver todos los servicios %s</a></div>%s</div></div>' % (u, cur(u), l, drop, icon('arrow'), promo))
        else:
            links += '<a href="%s"%s>%s</a>' % (u, cur(u), l)
    msub = ''.join('<a href="%s">%s%s</a>' % (su, icon(si), sl) for su, sl, si, sd in SUB)
    mob = ('<a href="index.html"%s><small>01</small>Inicio</a>' % cur('index.html') +
           '<div class="m-acc"><button type="button" class="m-acc-btn" aria-expanded="false" aria-controls="msub"><small>02</small>Servicios<svg class="caret" viewBox="0 0 10 6" aria-hidden="true"><path d="m1 1 4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>'
           '<div class="m-sub" id="msub"><div>%s<a class="m-all" href="servicios.html">Ver todos los servicios</a></div></div></div>' % msub +
           '<a href="cobertura.html"%s><small>03</small>Cobertura</a><a href="contacto.html"%s><small>04</small>Contacto</a>' % (cur('cobertura.html'), cur('contacto.html')))
    return ('<div class="top">' + ticker() + '<header class="site-header"><a class="brand" href="index.html" aria-label="Cerrajería Limited, inicio"><img src="assets/identidad.webp" alt="" width="52" height="52">'
            '<span>CERRAJERÍA<strong>LIMITED<span class="red">.</span></strong></span></a><nav id="main-nav" aria-label="Navegación principal">' + links + '</nav>'
            '<div class="head-actions"><a class="head-wa" href="' + WA + '" aria-label="WhatsApp">' + icon('wa') + '</a><a class="header-phone" href="' + TEL + '"><span class="status-dot"></span><span class="hp-label">Urgencias 24 h</span><b>' + PHONE_FMT + '</b></a>'
            '<button class="menu-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button></div><i class="progress" aria-hidden="true"></i></header></div>'
            '<div class="mnav" id="mnav" aria-hidden="true"><div class="mnav-inner"><nav aria-label="Menú móvil">' + mob + '</nav><div class="mnav-cta">'
            '<a class="button" href="' + TEL + '">Llamar ' + PHONE_FMT + '<span class="b-ic">' + icon('phone') + '</span></a><a class="button secondary" href="' + WA + '">WhatsApp<span class="b-ic">' + icon('wa') + '</span></a></div>'
            '<p class="mnav-note"><span class="status-dot"></span>Urgencias 24 h · 365 días · Guadalajara y Madrid</p></div></div>')


def footer():
    ex = ''.join('<a href="%s">%s</a>' % (u, l) for u, l in [('index.html', 'Inicio'), ('servicios.html', 'Servicios'), ('perdida-de-llaves.html', 'Pérdida de llaves'), ('copia-de-llaves.html', 'Copias de llaves'), ('apertura-de-vehiculos.html', 'Aperturas'), ('cobertura.html', 'Cobertura'), ('contacto.html', 'Contacto')])
    return ('<footer><div class="footer-top"><a class="brand" href="index.html"><img src="assets/identidad.webp" alt="" width="52" height="52"><span>CERRAJERÍA<strong>LIMITED<span class="red">.</span></strong></span></a>'
            '<p>Tu solución en cerrajería<br>de automoción.</p><a class="footer-phone" href="' + TEL + '">' + PHONE_FMT + ' ↗</a></div>'
            '<div class="footer-grid"><div><p class="eyebrow">EXPLORA</p>' + ex + '</div><div><p class="eyebrow">CONTACTO</p><a href="mailto:' + EMAIL + '">' + EMAIL + '</a><p>Calle Zaragoza 53<br>19005 Guadalajara</p><p>Guadalajara y Comunidad de Madrid<br>Urgencias 24 h · 365 días</p><p class="pay"><span>VISA</span><span>MASTERCARD</span></p></div>'
            '<div><p class="eyebrow">SIGUE A LIMITED</p><a target="_blank" rel="noopener" href="' + IG + '">Instagram ↗</a><a target="_blank" rel="noopener" href="' + FB + '">Facebook ↗</a><a target="_blank" rel="noopener" href="' + PA + '">Páginas Amarillas ↗</a></div></div>'
            '<div class="footer-bottom"><span>© 2026 Cerrajería Limited · Propuesta de web</span><a href="privacidad.html">Privacidad de esta demostración</a><span>Imágenes de ambiente ilustrativas</span></div></footer>'
            '<a class="floating-wa" href="' + WA + '" aria-label="Contactar por WhatsApp">' + icon('wa') + '<span>WhatsApp</span></a>'
            '<div class="mobile-contact"><a href="' + TEL + '">' + icon('phone') + 'Llamar ahora</a><a href="' + WA + '">' + icon('wa') + 'WhatsApp</a></div>')


CTA = ('<section class="cta-section"><div><p class="eyebrow">TU VEHÍCULO NO TIENE POR QUÉ ESPERAR</p><h2>Hablemos.<br><em>Y volvamos al camino.</em></h2></div><div>' +
       btn('Llamar ahora · ' + PHONE_FMT, TEL, '', 'phone') + btn('Consultar por WhatsApp', WA, 'secondary', 'wa') +
       '<p>Atención de urgencias 24 horas.<br>Consulta disponibilidad para tu ubicación.</p></div></section>')

HELP = ('<aside class="help-card" aria-label="Pedir ayuda rápida"><p class="eyebrow"><span class="live"></span>AYUDA AL INSTANTE</p><h2>¿Qué te ha pasado?</h2><p>Un toque y abres WhatsApp con el mensaje listo.</p>' +
        ''.join('<a href="%s">%s<span>%s</span>%s</a>' % (wa(m), icon(i), t, icon('arrow')) for t, i, m in [
            ('Perdí todas las llaves', 'key', 'Hola, he perdido todas las llaves de mi coche. ¿Podéis ayudarme?'),
            ('Llaves dentro del coche', 'car', 'Hola, me he quedado con las llaves dentro del coche. ¿Podéis abrirlo?'),
            ('Quiero una copia', 'copy', 'Hola, quiero hacer una copia de la llave de mi vehículo.'),
            ('Mando o cerradura fallan', 'lock', 'Hola, mi llave o cerradura no funciona bien. ¿Podéis revisarlo?')]) +
        '<a class="help-call" href="' + TEL + '">' + icon('phone') + 'Prefiero llamar · ' + PHONE_FMT + '</a></aside>')

CRUMB = {'index.html': ''}


def crumbs(filename, label):
    if filename == 'index.html':
        return ''
    return '<nav class="crumbs" aria-label="Migas de pan"><a href="index.html">Inicio</a><span>/</span><span aria-current="page">%s</span></nav>' % label


def build_page(filename, p, extra_cta=True):
    home_page = filename == 'index.html'
    hero = ('<section class="hero%s"><img class="hero-image" src="assets/%s.webp" alt="" fetchpriority="high"><div class="hero-shade"></div>'
            '<div class="hero-grid"><div class="hero-content">%s<p class="eyebrow"><span class="red-line"></span>%s</p><h1>%s</h1><p class="hero-intro">%s</p>'
            '<div class="hero-actions">%s%s</div><ul class="hero-badges"><li class="b-star">%s4,8 en Google</li><li>%s24 h · 365 días</li><li>%sA domicilio</li><li>%sSin daños</li></ul></div>%s</div>'
            '<div class="hero-bottom"><span>ESPECIALISTAS EN CERRAJERÍA DE VEHÍCULOS</span><a href="#contenido">DESCUBRE MÁS %s</a></div></section>') % (
        ' home-hero' if home_page else '', p['img'], crumbs(filename, p['title']),
        p['kicker'], p['heading'], p['intro'], btn('Llamar · ' + PHONE_FMT, TEL, '', 'phone'), btn('Consultar por WhatsApp', WA, 'secondary', 'wa'),
        icon('star'), icon('clock'), icon('home'), icon('shield'), HELP if home_page else '', '<span>↓</span>')
    faqs = []
    schema = [{'@context': 'https://schema.org', '@type': 'Locksmith', 'name': 'Cerrajería Limited', 'telephone': '+34' + PHONE, 'email': EMAIL,
               'address': {'@type': 'PostalAddress', 'streetAddress': 'Calle Zaragoza 53', 'addressLocality': 'Guadalajara', 'postalCode': '19005', 'addressCountry': 'ES'},
               'areaServed': ['Guadalajara', 'Comunidad de Madrid'], 'openingHours': 'Mo-Su 00:00-23:59', 'paymentAccepted': 'Tarjeta de crédito', 'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': '4.8', 'reviewCount': '38'}}]
    schema_html = ''.join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False) for s in schema)
    body = p['body'] + (related(filename) if filename in SERVICE_PAGES and filename != 'servicios.html' else '')
    return ('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s | Cerrajería Limited</title>'
            '<meta name="description" content="%s"><meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="Cerrajería Limited"><meta property="og:title" content="%s | Cerrajería Limited"><meta property="og:description" content="%s"><meta property="og:url" content="' + SITE + '%s"><meta property="og:image" content="' + SITE + 'assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Cerrajería Limited, cerrajería de coches 24 horas en Guadalajara y Madrid"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#09090b"><meta name="robots" content="noindex,nofollow"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">'
            '<link rel="stylesheet" href="assets/style.css"><script>document.documentElement.classList.add("js")</script><script defer src="assets/app.js"></script>%s</head><body>'
            '<a class="skip-link" href="#contenido">Saltar al contenido</a>%s<main>%s<div id="contenido">%s</div>%s</main>%s</body></html>') % (
        p['title'], p['intro'], p['title'], p['intro'], '' if filename == 'index.html' else filename, schema_html, header(filename), hero, body, CTA if extra_cta else '', footer())


for fn, p in pages.items():
    (D / fn).write_text(build_page(fn, p), encoding='utf-8')

privacy = dict(title='Privacidad de la demostración', kicker='INFORMACIÓN DE ESTA PROPUESTA', heading='Una consulta.<br>Con <em>claridad.</em>',
               intro='Información sobre el funcionamiento de esta demostración y los canales de contacto que enlaza.', img='hero',
               body='<section class="section prose"><h2>Privacidad de esta demostración</h2><p>Esta web es una propuesta de diseño para Cerrajería Limited. No incorpora un sistema propio de almacenamiento de consultas, registro de usuarios, publicidad ni herramientas de analítica.</p><h3>Consulta por WhatsApp</h3><p>El formulario prepara un mensaje en tu navegador y abre un enlace a WhatsApp. No envía ni guarda por sí mismo los datos introducidos. Revisa el mensaje y envíalo solo si deseas contactar con el negocio. El uso de WhatsApp está sujeto a las condiciones y privacidad de ese servicio.</p><h3>Enlaces externos</h3><p>Los enlaces a redes sociales, mapas y directorios llevan a servicios ajenos a esta demostración, con sus propias condiciones. Las llamadas y correos se gestionan mediante la aplicación de tu dispositivo.</p><h3>Antes de una publicación comercial</h3><p>El titular deberá validar los datos de contacto, la información comercial y completar la identificación legal y la política de privacidad que correspondan a la web definitiva.</p><h3>Imágenes y contenido</h3><p>El logo procede del material aportado. Las fotografías de ambiente son ilustraciones creadas para esta propuesta; no se presentan como fotografías del personal, instalaciones o vehículos reales del negocio.</p></section>')
html = build_page('privacidad.html', privacy, extra_cta=False)
(D / 'privacidad.html').write_text(html, encoding='utf-8')

(A / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0a0a0b"/><circle cx="23" cy="23" r="10" fill="none" stroke="#f22431" stroke-width="7"/><path d="m30 30 20 20m-6-6 5-5m-11-1 5-5" stroke="#fff" stroke-width="6"/></svg>')
print('Built', len(pages) + 1, 'HTML pages')
