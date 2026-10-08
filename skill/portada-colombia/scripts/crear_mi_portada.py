#!/usr/bin/env python3
"""Arma la skill personalizada «mi-portada-colombia» a partir de un perfil.

Uso:
    python3 crear_mi_portada.py --perfil perfil.json --salida carpeta/

El perfil es un JSON con:
    {"temas": [...], "palabras": [...], "departamento": "Santander" | ""}

Produce <salida>/mi-portada-colombia.zip con la carpeta mi-portada-colombia/
adentro, lista para subir en Claude (Configuración › Capacidades › Skills).

Solo usa la biblioteca estándar de Python 3.9 o superior.
Hecho por Estado X. Licencia MIT.
"""

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

NOMBRE = "mi-portada-colombia"
RAIZ = Path(__file__).resolve().parent.parent  # carpeta de la skill
MAX_TEMAS = 6
MAX_PALABRAS = 8
MAX_LARGO_PALABRA = 60


def leer_tabla(archivo: Path, seccion: str = "") -> list:
    """Devuelve la primera columna de las tablas Markdown del archivo.

    Si se da `seccion`, solo lee la tabla que sigue a ese título (## ...).
    """
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    dentro = not seccion
    valores = []
    for linea in lineas:
        if linea.startswith("## "):
            dentro = (not seccion) or linea[3:].strip() == seccion
            continue
        if not dentro or not linea.startswith("|"):
            continue
        celda = linea.strip("|").split("|")[0].strip()
        if not celda or set(celda) <= set("-: ") or celda in ("Tema", "Departamento", "Medio"):
            continue
        valores.append(celda)
    return valores


def limpiar(texto: str) -> str:
    """Quita saltos de línea y caracteres que podrían romper el Markdown o el YAML."""
    texto = re.sub(r"[\r\n\t]+", " ", str(texto))
    texto = re.sub(r"[<>`|#*\[\]{}\"\\]", "", texto)
    return texto.strip()


def validar(perfil: dict, temas_validos: list, deptos_validos: list) -> dict:
    errores = []
    temas = perfil.get("temas") or []
    if not isinstance(temas, list) or not temas:
        errores.append("Falta escoger al menos un tema.")
        temas = []
    temas = [t for t in temas if isinstance(t, str)]
    desconocidos = [t for t in temas if t not in temas_validos]
    if desconocidos:
        errores.append("Temas que no están en la lista: " + ", ".join(desconocidos))
    if len(temas) > MAX_TEMAS:
        errores.append(f"Máximo {MAX_TEMAS} temas (llegaron {len(temas)}).")

    palabras = perfil.get("palabras") or []
    if not isinstance(palabras, list):
        errores.append("«palabras» debe ser una lista.")
        palabras = []
    palabras = [limpiar(p)[:MAX_LARGO_PALABRA] for p in palabras if limpiar(p)]
    if len(palabras) > MAX_PALABRAS:
        errores.append(f"Máximo {MAX_PALABRAS} palabras propias (llegaron {len(palabras)}).")

    depto = (perfil.get("departamento") or "").strip()
    if depto and depto not in deptos_validos:
        errores.append(f"Departamento desconocido: {depto}. Usa uno de references/medios.md.")

    if errores:
        raise ValueError("\n".join(errores))
    return {"temas": temas, "palabras": palabras, "departamento": depto}


def texto_perfil(p: dict) -> str:
    hora_col = datetime.now(timezone(timedelta(hours=-5)))
    temas = "\n".join(f"- {t}" for t in p["temas"])
    palabras = "\n".join(f"- {w}" for w in p["palabras"]) or "- (ninguna)"
    depto = p["departamento"] or "Solo nacional"
    return (
        "# Perfil de mi portada\n\n"
        "configurado: sí\n"
        f"creado: {hora_col:%d/%m/%Y}\n\n"
        f"## Temas\n{temas}\n\n"
        f"## Palabras propias\n{palabras}\n\n"
        f"## Región\n- {depto}\n"
    )


def descripcion(p: dict) -> str:
    partes = ", ".join(p["temas"])
    if p["departamento"]:
        partes += f" y noticias de {p['departamento']}"
    return (
        f"Arma mi portada de noticias de Colombia con mis temas ({partes}). "
        "Úsala con «mi portada», «noticias de hoy», «qué pasó hoy» o «cambia mis temas»."
    )[:1000]


def armar(perfil_json: Path, salida: Path) -> Path:
    temas_validos = leer_tabla(RAIZ / "references" / "temas.md")
    deptos_validos = leer_tabla(RAIZ / "references" / "medios.md", "Por departamento")
    perfil = validar(json.loads(perfil_json.read_text(encoding="utf-8")), temas_validos, deptos_validos)

    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / NOMBRE
        shutil.copytree(
            RAIZ, destino,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "perfil.md", ".DS_Store"),
        )
        skill_md = destino / "SKILL.md"
        texto = skill_md.read_text(encoding="utf-8")
        cabecera, cuerpo = texto.split("---\n", 2)[1:]
        cabecera = re.sub(r"^name: .*$", f"name: {NOMBRE}", cabecera, flags=re.M)
        cabecera = re.sub(r"^description: .*$", f"description: {descripcion(perfil)}", cabecera, flags=re.M)
        skill_md.write_text(f"---\n{cabecera}---\n{cuerpo}", encoding="utf-8")
        (destino / "perfil.md").write_text(texto_perfil(perfil), encoding="utf-8")

        salida.mkdir(parents=True, exist_ok=True)
        zip_path = salida / f"{NOMBRE}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(destino.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(Path(tmp)).as_posix())
    return zip_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Arma la skill mi-portada-colombia.")
    ap.add_argument("--perfil", required=True, type=Path, help="JSON con temas, palabras y departamento")
    ap.add_argument("--salida", default=Path("."), type=Path, help="carpeta donde queda el .zip")
    args = ap.parse_args()
    try:
        ruta = armar(args.perfil, args.salida)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"No se pudo armar la skill:\n{e}", file=sys.stderr)
        return 1
    print(f"Listo: {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
