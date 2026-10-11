# Cerrajería Limited — propuesta de web

Ocho páginas HTML independientes, sin instalación ni compilación para visualizarlas. El sitio completo está en `dist/`.

## Vista local

Abre `dist/index.html` o sirve la carpeta con `python -m http.server 8080 --directory dist`.

## Edición

Contenido y plantillas: `build.py`. Ejecuta `python build.py` para regenerar los HTML. Estilos: `dist/assets/style.css`. Menú y consulta de WhatsApp: `dist/assets/app.js`.

## Validación

`python validate.py` comprueba enlaces, anclas, imágenes, fuente y encabezados. `node --check dist/assets/app.js` comprueba sintaxis JavaScript.

## Información editorial

Se ha priorizado el 672 826 060, presente en el logo aportado, la ficha de Páginas Amarillas y la web actual. Hay material que usa 624 218 073. Confirmar con el titular antes de la publicación comercial.

Dirección y correo contrastados en https://5f740d2b821445aa999e354368ee82a1.beedigitalwebs.com/ : Calle Zaragoza 53, Guadalajara 19005; cerrajerialimited@gmail.com.

Servicios y cobertura contrastados con la ficha aportada de Páginas Amarillas y la web actual. Capturas facilitadas utilizadas como información, no como banners de texto.

No se publican precios de promociones al existir importes y periodos distintos. No hay reseñas ni estadísticas inventadas.

El formulario no guarda datos ni envía mensajes automáticamente: abre WhatsApp con texto preparado. La demostración está marcada como no indexable. La página de privacidad describe el funcionamiento de la demostración; para una web comercial el titular debe completar la identificación legal que corresponda.

## Imágenes

Logo aportado conservado en `dist/assets/identidad.webp`. Imágenes ilustrativas creadas con la herramienta integrada de generación de imágenes, optimizadas en WebP:

- `dist/assets/hero.webp`: fotografía cinematográfica de coche negro y llave, luces rojas, espacio oscuro a la izquierda, sin texto.
- `dist/assets/keys.webp`: técnico con guantes trabajando con llave, cortadora y equipo de diagnóstico, paleta negro y rojo, sin texto.
- `dist/assets/mobile.webp`: asistencia de cerrajería móvil al atardecer, furgoneta y técnico junto a coche, sin logotipos ni texto.

Los prompts completos se conservan en `image-prompts.json`. Las imágenes son ambientales y no representan las instalaciones, empleados o vehículos reales del negocio.

Tipografía: Barlow Condensed Bold, de Google Fonts, almacenada localmente.
