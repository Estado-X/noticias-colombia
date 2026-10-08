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
6. Arma su skill con el script, escribiendo el perfil en un archivo JSON:

   ```bash
   python3 scripts/crear_mi_portada.py --perfil perfil.json --salida <carpeta de archivos para descargar>
   ```

   El JSON tiene esta forma:

   ```json
   {"temas": ["Economía y empleo", "Ambiente y clima"],
    "palabras": ["Catatumbo"],
    "departamento": "Santander"}
   ```

   `departamento` va vacío (`""`) si escogió solo nacional. Usa los nombres exactos de `temas.md` y `medios.md`. El script valida el perfil y produce `mi-portada-colombia.zip`.
7. Entrega el `.zip` como archivo para descargar y explica cómo instalarlo:
   1. Descarga el archivo `mi-portada-colombia.zip`. No lo descomprimas.
   2. En Claude, ve a **Configuración › Capacidades › Skills** y pulsa **Subir skill**. Necesitas tener activa la ejecución de código.
   3. Desactiva la skill `portada-colombia` para que no se cruce con la tuya.
   4. Activa la **búsqueda web** en el chat y escribe «mi portada».
8. Ofrece armar ya una primera portada con el perfil que escogió (sigue el modo portada con esas respuestas).

Si el script no corre en tu entorno, explica que la ejecución de código debe estar activa y no intentes armar el `.zip` a mano.

## Modo portada

Objetivo: un tablero visual con lo más importante de las últimas 24 horas para los temas y la región de `perfil.md`, con un resumen de tres líneas arriba.

Si la persona pide «cambia mis temas» o «cambia mi región», vuelve al modo instalación: el script arma una skill nueva con el perfil nuevo, que reemplaza la anterior.

### 1. Buscar

- Necesitas la **búsqueda web**. Si no la tienes, dilo en una línea y pide a la persona que la active. No armes una portada de memoria.
- Por cada tema del perfil, busca con los términos de `references/temas.md` más «Colombia» y la fecha de hoy. Por cada palabra propia, una búsqueda aparte. Si hay departamento, busca además «noticias <departamento> hoy» y prueba con los medios de ese departamento en `references/medios.md` (por ejemplo `site:vanguardia.com`).
- Prefiere los medios de `references/medios.md`. Puedes usar otros medios colombianos reconocidos. No uses agregadores (Google Noticias, MSN, Yahoo), sitios de contenido copiado ni redes sociales.
- Si puedes abrir la página de la noticia, confirma la fecha y que el titular coincide.

### 2. Escoger

- Solo noticias de las **últimas 24 horas**. Si un tema queda vacío, amplía a 48 horas y márcalo. Si sigue vacío, deja la columna con «Sin noticias nuevas sobre este tema hoy».
- Entre 3 y 6 noticias por columna. Sin repetir el mismo hecho en dos columnas: déjalo donde más pese.
- Una sola noticia por hecho, aunque la cuenten varios medios. Prefiere la fuente que lo informó primero o la del departamento.
- Cada noticia lleva: titular tal como lo publicó el medio, nombre del medio, fecha y hora (si la hay), enlace directo y **una línea propia** de por qué importa.

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
3. Muestra el resultado como una página (artefacto HTML). No cambies el diseño ni agregues librerías.
4. Debajo, en el chat, escribe solo el resumen de tres líneas y una línea con «Fuentes:» y los medios usados.

## Archivos

- `references/temas.md`: los temas y sus términos de búsqueda.
- `references/medios.md`: medios nacionales y regionales verificados.
- `assets/tablero.html`: plantilla del tablero.
- `scripts/crear_mi_portada.py`: arma la skill personalizada.
- `perfil.md`: el perfil (solo en la skill personalizada).

Hecho por Estado X (https://estadox.com). Licencia MIT. Inspirado en newsnow de ourongxing (MIT).
