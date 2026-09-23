/* ============================================================
   CONFIG ÚNICA DEL EVENTO — XV Años Paula Victoria Rivera Chávez
   Cambiar SOLO aquí. Todas las páginas leen de window.EVENT_CONFIG.
   ============================================================ */
window.EVENT_CONFIG = {
    // ── Identidad ─────────────────────────────────────────────
    slug:        'xv-paula-victoria',
    nombre:      'Paula Victoria Rivera Chávez',
    nombreCorto: 'Paula Victoria',
    tipo:        'XV Años',

    // ── Fecha (mes en base 0: 8 = septiembre) ─────────────────
    fechaEvento: new Date(2026, 8, 26, 18, 0, 0),
    fechaTexto:  'Sábado 26 de septiembre de 2026',

    // ── Contacto ──────────────────────────────────────────────
    telefono:        '524779203776',                  // WhatsApp FORO 7
    contactoTitular: 'Mayra Lizbeth González Ramírez', // contratante

    // ── Paquete contratado ────────────────────────────────────
    // Tomado de contrato.html: "PAQUETE COMPLETO" + dron 4K
    // bonificado (el dron ya venía pagado por la prima).
    paquete: {
        nombre:          'Fotografía y Video · Paquete Completo (con dron)',
        fotosImpresas:   100,
        medidaImpresion: '5x7 pulgadas',
        ampliaciones:    1,
        videoHoras:      'Película en USB editada y musicalizada',
        incluye: [
            '100 fotografías impresas en 5x7 pulgadas',
            'Película en USB editada y musicalizada',
            'Videoclip para proyección durante el evento',
            'Fotografía ampliada 40x50 cm con marco',
            'Tomas aéreas con dron 4K (cortesía)',
            'Cobertura: 1 hora de ceremonia + 6 horas de fiesta',
            'Sesión fotográfica previa (18 de septiembre, Parque Explora)'
        ]
    },

    // ── Límites del selector ──────────────────────────────────
    limiteImpresion:    100,
    limiteAmpliacion:   1,      // la ampliación 40x50 con marco
    limiteAlbum:        null,   // null = sin límite
    costoFotoAdicional: 15,     // MXN por foto impresa extra

    // ── Supabase ──────────────────────────────────────────────
    supabaseUrl:  'https://nzpujmlienzfetqcgsxz.supabase.co',
    supabaseAnon: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56cHVqbWxpZW56ZmV0cWNnc3h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2ODYzMzYsImV4cCI6MjA5MDI2MjMzNn0.xl3lsb-KYj5tVLKTnzpbsdEGoV9ySnswH4eyRuyEH1s'
};

/* ============================================================
   HERRAMIENTAS DEL SELECTOR
   Este arreglo define TODO: tarjetas de conteo, botones de
   filtro, botones del modal, colores, textos de ayuda y los
   filtros válidos de album.html?filtro=…
   Paula SÍ lleva "Ampliación" (su Paquete Completo incluye una
   fotografía ampliada 40x50 cm con marco).
   ============================================================ */
(function (C) {
window.HERRAMIENTAS = [
    {
        id:      'impresion',
        icono:   '📸',
        nombre:  'Impresión',
        textoBtn:'Impresión (' + C.paquete.medidaImpresion.replace(' pulgadas', '') + ')',
        limite:  C.limiteImpresion,
        // Como se lee en el encabezado del selector.
        fraseIncluida: C.paquete.fotosImpresas + ' fotos impresas en ' + C.paquete.medidaImpresion,
        columna: 'impresion',      // columna booleana en Supabase
        ayuda:   'Marca las fotos que quieres <strong>impresas en papel tamaño ' + C.paquete.medidaImpresion +
                 '</strong>. Tu paquete incluye ' + C.limiteImpresion + '. Si marcas más, abajo aparece un aviso naranja ' +
                 'con el costo extra ($' + C.costoFotoAdicional + ' MXN por foto adicional). Estas son las fotos que ' +
                 'recibes físicas en tu caja impresa.'
    },
    {
        id:      'ampliacion',
        icono:   '🖼️',
        nombre:  'Ampliación',
        textoBtn:'Ampliación 40x50',
        limite:  C.limiteAmpliacion,
        columna: 'ampliacion',     // columna booleana en Supabase
        ayuda:   'La foto que quieres <strong>ampliada a 40x50 cm y enmarcada</strong>. Tu paquete incluye ' +
                 '<strong>1</strong>, así que elige la que más te guste: es la que va a colgarse en tu casa. ' +
                 'Si marcas más de una te decimos cuánto cuesta cada ampliación extra.'
    },
    {
        id:      'album',
        icono:   '📖',
        nombre:  'Álbum Digital',
        textoBtn:'Álbum Digital',
        limite:  null,
        columna: 'datos.album',    // se guarda dentro del jsonb "datos"
        ayuda:   'Las fotos que quieres en tu <strong>álbum digital</strong>: la galería en línea que puedes compartir por WhatsApp con familia y amigos. No tiene límite y no cuesta extra. Marca aquí tus favoritas aunque ya las hayas marcado para impresión.'
    },
    {
        id:      'descartada',
        icono:   '❌',
        nombre:  'Descartadas',
        textoBtn:'Descartar',
        limite:  null,
        columna: 'descartada',
        ayuda:   'Fotos que <strong>no quieres</strong> (saliste parpadeando, movida, repetida…). Al descartarlas <strong>desaparecen de la vista general</strong> para que no estorben mientras eliges. No se borran: siempre puedes verlas en el filtro «Descartadas» y quitarles la marca si te arrepientes.'
    }
];
})(window.EVENT_CONFIG);
