#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Regenera js/photos-2.js a partir de los archivos de la carpeta img/.

Uso:
    python generate_photo_list.py

Estructura esperada:
    img/           -> foto completa (se abre en el modal / lightbox)
    img/thumb/          -> miniatura del mismo nombre (se usa en la rejilla)
    img/<sub>/ + img/<sub>/thumb/  -> igual, por subcarpeta (ej. misa-y-fiesta)

Si una foto no tiene miniatura, la rejilla usa la completa.
Respeta el orden de la lista actual (foto_index en Supabase) y agrega las
fotos nuevas al final, en orden natural. Acepta .webp .jpg .jpeg .png .avif.
Ver D:\\eventos\\HERRAMIENTAS_FOTOS.md para el convertidor JPEG -> WebP.
"""

import os
import re
import sys
import glob
import hashlib

try:
    from urllib.parse import quote          # py3
except ImportError:
    from urllib import quote               # py2

AQUI    = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, 'img')
THUMBS  = os.path.join(CARPETA, 'thumb')
SALIDA  = os.path.join(AQUI, 'js', 'photos-2.js')
EXTS    = ('.webp', '.jpg', '.jpeg', '.png', '.avif')

CABECERA = """/* ============================================================
   LISTA DE FOTOS - XV Anos Paula Victoria Rivera Chávez
   NO editar a mano: se regenera con  python generate_photo_list.py
   Fotos: %d   |   Con miniatura: %d
   ============================================================ */

// Foto completa: se abre en el modal del selector y en el lightbox.
window.PHOTOS = [
%s
];

// Miniatura: es lo que carga la rejilla. Si falta, cae a la completa.
window.PHOTO_THUMBS = [
%s
];

// Nombre de archivo original (mismo orden). Se guarda en Supabase
// (datos.filename) para localizar el archivo maestro.
window.PHOTO_FILES = [
%s
];
"""


def clave_natural(nombre):
    partes = re.split(r'(\d+)', nombre.lower())
    return [int(p) if p.isdigit() else p for p in partes]


def listar(carpeta):
    fs = [f for f in os.listdir(carpeta)
          if f.lower().endswith(EXTS)
          and not f.startswith('.')
          and os.path.isfile(os.path.join(carpeta, f))]
    return sorted(fs, key=clave_natural)


def orden_actual():
    """PHOTO_FILES de la lista publicada (js/photos.*.js), en su orden."""
    for js in glob.glob(os.path.join(AQUI, 'js', 'photos.*.js')):
        with open(js, 'r', encoding='utf-8') as fh:
            m = re.search(r'window\.PHOTO_FILES\s*=\s*\[(.*?)\];', fh.read(), re.S)
        if m:
            return re.findall(r'"([^"]+)"', m.group(1))
    return []


def main():
    if not os.path.isdir(CARPETA):
        print('No existe la carpeta: %s' % CARPETA)
        return 1

    archivos = listar(CARPETA)
    for sub in sorted(os.listdir(CARPETA), key=clave_natural):
        if sub != 'thumb' and os.path.isdir(os.path.join(CARPETA, sub)):
            archivos += ['%s/%s' % (sub, f) for f in listar(os.path.join(CARPETA, sub))]

    # El indice de cada foto es el foto_index guardado en Supabase: se respeta
    # el orden de la lista actual y las fotos nuevas se agregan AL FINAL.
    previas = orden_actual()
    presentes = set(archivos)
    archivos = ([f for f in previas if f in presentes]
                + [f for f in archivos if f not in set(previas)])

    if not archivos:
        print('Sin imagenes en %s (se genera lista vacia).' % CARPETA)

    # Las rutas van codificadas: hay archivos con espacios y parentesis
    # (IMG_1894 (2).webp) que sin %20 dan 404 en GitHub Pages.
    url = lambda p: quote(p, safe='/')

    con_thumb = 0
    thumbs = []
    for f in archivos:
        carpeta, _, nombre = f.rpartition('/')
        t = '%s/thumb/%s' % (carpeta, nombre) if carpeta else 'thumb/%s' % nombre
        if os.path.isfile(os.path.join(CARPETA, t)):
            thumbs.append(url('img/%s' % t))
            con_thumb += 1
        else:
            thumbs.append(url('img/%s' % f))

    bloque = lambda xs: ',\n'.join('    "%s"' % x for x in xs)

    with open(SALIDA, 'w', encoding='utf-8') as fh:
        fh.write(CABECERA % (
            len(archivos), con_thumb,
            bloque(url('img/%s' % f) for f in archivos),
            bloque(thumbs),
            bloque(archivos),
        ))

    # El nombre lleva un hash del contenido: Cloudflare cachea un año
    # y el ?v= no lo invalida, así que cada cambio necesita URL nueva.
    with open(SALIDA, 'r', encoding='utf-8') as fh:
        firma = hashlib.sha1(fh.read().encode('utf-8')).hexdigest()[:8]
    nuevo = os.path.join(AQUI, 'js', 'photos.%s.js' % firma)
    # Ojo: el glob también casa con la salida recién escrita. Borrarla
    # aquí deja sin archivo al rename de abajo.
    intocables = {os.path.abspath(nuevo), os.path.abspath(SALIDA)}
    for viejo in glob.glob(os.path.join(AQUI, 'js', 'photos*.js')):
        if os.path.abspath(viejo) not in intocables:
            os.remove(viejo)
    if not os.path.exists(nuevo):
        os.rename(SALIDA, nuevo)
    nombre_js = os.path.basename(nuevo)

    # Actualizar las páginas que lo cargan
    for pagina in ('index.html', 'selector.html', 'album.html', 'sw.js'):
        ruta = os.path.join(AQUI, pagina)
        if not os.path.exists(ruta):
            continue
        with open(ruta, 'r', encoding='utf-8') as fh:
            txt = fh.read()
        nvo = re.sub(r'js/photos[^"\']*\.js', 'js/' + nombre_js, txt)
        if nvo != txt:
            with open(ruta, 'w', encoding='utf-8', newline='') as fh:
                fh.write(nvo)

    print('OK  %d fotos (%d con miniatura) -> js/%s' % (len(archivos), con_thumb, nombre_js))
    if archivos and con_thumb < len(archivos):
        print('AVISO: %d fotos sin miniatura en img/thumb/' % (len(archivos) - con_thumb))
    print('Las paginas que lo cargan ya quedaron apuntando al archivo nuevo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
