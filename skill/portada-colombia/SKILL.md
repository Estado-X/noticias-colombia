---
name: portada-colombia
description: Arma una portada de noticias de Colombia con los temas y la región de cada persona. La primera vez pregunta temas y departamento y entrega la skill personalizada «mi-portada-colombia» para instalar. Úsala con «instala mi portada», «arma mi portada de noticias», «mi portada», «noticias de hoy» o «qué pasó hoy en Colombia».
---

# Portada de noticias de Colombia

Esta skill tiene dos modos. Mira el archivo `perfil.md` que está junto a este archivo:

- Si no existe, o dice `configurado: no`, estás en **modo instalación**.
- Si dice `configurado: sí`, estás en **modo portada**.

Habla siempre en español de Colombia, claro y cálido, sin jerga técnica. Fechas en dd/mm/aaaa.

## Modo instalación

Objetivo: preguntar a la persona qué le interesa y entregarle su propia skill, `mi-portada-colombia`, lista para subir a Claude.

1. Saluda en una línea y explica que vas a hacerle tres preguntas para armar su portada.
2. **Temas.** Muestra la lista de `references/temas.md` (solo los nombres, numerados) y pide que escoja los que quiera, entre 1 y 6. Si tu entorno tiene preguntas de opción múltiple, úsalas.
3. **Palabras propias.** Pregunta si quiere seguir algo específico: un lugar, una persona pública, un proyecto de ley, una empresa. Ejemplos: «Catatumbo», «reforma pensional», «metro de Bogotá». Máximo 8. Puede no poner ninguna.
4. **Región.** Pregunta si quiere solo noticias nacionales o también las de un departamento. Lista de departamentos en `references/medios.md`.
5. Repite en un párrafo lo que escogió y pide confirmación.
6. Arma su skill con el script de esta skill. Escribe el perfil en un archivo JSON dentro de una carpeta de trabajo donde puedas escribir (no dentro de la carpeta de la skill, que puede ser de solo lectura) y corre el script con su ruta completa:

   ```bash
   python3 <carpeta de esta skill>/scripts/crear_mi_portada.py --perfil <carpeta de trabajo>/perfil.json --salida <carpeta de archivos para descargar>
   ```

   El JSON tiene esta forma:

   ```json
   {"temas": ["Economía y empleo", "Ambiente y clima"],
    "palabras": ["Catatumbo"],
    "departamento": "Santander"}
   ```

   `departamento` va vacío (`""`) si escogió solo nacional. Usa los nombres exactos de `temas.md` y `medios.md`. El script valida el perfil y produce `mi-portada-colombia.zip`. Si responde con un error, corrige el perfil con la persona y vuelve a correrlo.
7. Entrega el `.zip` como archivo para descargar y explica cómo instalarlo:
   1. Descarga el archivo `mi-portada-colombia.zip`. No lo descomprimas.
   2. En Claude, ve a **Configuración › Capacidades › Skills** y pulsa **Subir skill**. Necesitas tener activa la ejecución de código.
   3. Desactiva la skill `portada-colombia` para que no se cruce con la tuya.
   4. Activa la **búsqueda web** en el chat y escribe «mi portada».
8. Ofrece armar ya una primera portada con el perfil que escogió (sigue el modo portada con esas respuestas).

Si el script no corre en tu entorno, explica que la ejecución de código debe estar activa y no intentes armar el `.zip` a mano.

## Modo portada

Objetivo: un tablero visual con lo más importante de las últimas 24 horas para los temas y la región de `perfil.md`, con un resumen de tres líneas arriba.

Si la persona pide «cambia mis temas» o «cambia mi región», vuelve al modo instalación y arma una skill nueva. Explícale que, antes de subirla, debe borrar la `mi-portada-colombia` que tiene instalada (las dos se llaman igual).

### 1. Buscar

- Necesitas la **búsqueda web**. Si no la tienes, dilo en una línea y pide a la persona que la active. No armes una portada de memoria.
- Usa la hora de Colombia (UTC−5). Si no sabes la hora actual, deja `hora` vacía y toma como ventana desde las 00:00 de ayer.
- Busca con frases en lenguaje natural y la fecha en letras, por ejemplo «noticias de salud en Colombia hoy 8 de octubre de 2026». Los resultados casi nunca traen la fecha: **abre cada candidata** y confirma fecha y hora en la página del artículo.
- Para el departamento, busca «<nombre del medio> <departamento> últimas noticias» con los medios de `references/medios.md` y abre la sección que aparezca en los resultados. No escribas direcciones a mano: abre solo las que salgan en una búsqueda.
- Tope de trabajo: máximo 2 búsquedas por tema, 1 por palabra propia y 2 para el departamento, y máximo 15 páginas abiertas. Si con eso no llenas una columna, déjala con lo que tengas y dilo en `nota`.
- Prefiere los medios de `references/medios.md`. Puedes usar otros medios colombianos reconocidos, incluidos los especializados de esa lista. Descarta agregadores (Google Noticias, MSN, Yahoo), redes sociales, sitios que copian contenido, blogs en inglés sobre Colombia, calendarios, guías turísticas y páginas sin autor ni fecha.

### 2. Escoger

- Noticias de las **últimas 24 horas**. Si una columna tiene menos de 3, complétala con noticias de hasta 48 horas y avísalo en `nota` («Incluye noticias de ayer»). Si aun así hay menos de 3, deja las que haya. Si no hay ninguna, deja la columna vacía: el tablero dirá «Sin noticias nuevas sobre este tema hoy».
- No te fíes de «hace X horas» ni de la hora de los metadatos sin revisar la zona: si la página da la hora en UTC, réstale 5. Si no estás seguro de la hora, pon solo la fecha.
- Entre 3 y 6 noticias por columna. Un mismo hecho va una sola vez, en la columna donde más pese, con la versión de un medio de la lista que caiga dentro de la ventana (si hay varias, la del departamento o la más completa).
- **Orden de las columnas:** los temas del perfil, luego «Lo que sigues» (las palabras propias) y al final el departamento.
- En «Lo que sigues», máximo 2 noticias por palabra; empieza el campo `porque` con la palabra entre corchetes, por ejemplo «[Catatumbo] …». En `nota`, di cuáles palabras no tuvieron noticias hoy.
- En la columna del departamento pon lo más útil para quien vive allí: servicios públicos, obras, salud, seguridad y decisiones de la alcaldía o la gobernación. Evita farándula y resultados deportivos. Una noticia del departamento va en esa columna aunque sea de un tema del perfil.
- Cada noticia lleva: el titular tal como aparece en la página del artículo (si te llega cortado, usa el del resultado de búsqueda; nunca lo completes de memoria), el nombre del medio, la fecha y hora en formato dd/mm/aaaa h:mm a. m./p. m., el enlace directo y **una línea propia** de por qué importa.

### 3. Reglas de contenido

- **No inventes.** Nada de titulares, cifras, fechas ni enlaces que no estén en los resultados. Si dudas de un dato, déjalo por fuera.
- **No copies los artículos.** Solo el titular y tu línea propia. Nada de párrafos del medio.
- **Sin opinión política.** Resume los hechos; no califiques a personas ni partidos.
- Si la búsqueda trae poco, dilo con honestidad en el resumen.

### 4. Armar el tablero

1. Lee `assets/tablero.html`. Es la plantilla con el diseño de Estado X.
2. Reemplaza el contenido del bloque `<script id="datos" type="application/json">` por un JSON con esta forma:

   ```json
   {
     "fecha": "08/10/2026",
     "hora": "7:30 a. m.",
     "resumen": ["Línea 1.", "Línea 2.", "Línea 3."],
     "columnas": [
       {"titulo": "Economía y empleo",
        "nota": "",
        "noticias": [
          {"titular": "…", "medio": "La República", "fecha": "08/10/2026 6:12 a. m.",
           "url": "https://…", "porque": "…"}
        ]}
     ],
     "perfil": "Economía y empleo · Ambiente y clima · Santander"
   }
   ```

   - Una columna por tema, en el orden del perfil. Las palabras propias van en una columna «Lo que sigues». Si hay departamento, una columna con su nombre.
   - `nota` sirve para avisos como «Amplié a 48 horas».
   - El `resumen` son tres frases tuyas sobre lo más importante del día para esta persona.
   - Dentro del bloque, escribe `<\/` en lugar de `</` en cualquier texto (por ejemplo en un titular que traiga `</`). Así ningún dato puede cerrar el bloque.
3. Muestra el resultado como una página (artefacto HTML). No cambies el diseño ni agregues librerías.
4. Debajo, en el chat, escribe solo el resumen de tres líneas y una línea con «Fuentes:» y los medios usados.

## Archivos

- `references/temas.md`: los temas y sus términos de búsqueda.
- `references/medios.md`: medios nacionales y regionales verificados.
- `assets/tablero.html`: plantilla del tablero.
- `scripts/crear_mi_portada.py`: arma la skill personalizada.
- `perfil.md`: el perfil (solo en la skill personalizada).

Hecho por Estado X (https://estadox.com). Licencia MIT. Inspirado en newsnow de ourongxing (MIT).
