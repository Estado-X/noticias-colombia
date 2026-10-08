#!/usr/bin/env python3
"""Arma los archivos de descarga y el ejemplo a partir de skill/portada-colombia/.

    python3 scripts/empacar.py

- descargas/portada-colombia.zip: la skill lista para subir a Claude.
- ejemplo/index.html: la plantilla del tablero llena con ejemplo/datos-ejemplo.json.

Solo usa la biblioteca estándar de Python 3.9 o superior.
"""
import json
import re
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "skill" / "portada-colombia"


def empacar() -> Path:
    destino = RAIZ / "descargas" / "portada-colombia.zip"
    destino.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and f.name != "perfil.md":
                info = zipfile.ZipInfo(f.relative_to(SKILL.parent).as_posix(), (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
    return destino


def ejemplo() -> Path:
    plantilla = (SKILL / "assets" / "tablero.html").read_text(encoding="utf-8")
    datos = json.loads((RAIZ / "ejemplo" / "datos-ejemplo.json").read_text(encoding="utf-8"))
    bloque = json.dumps(datos, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html = re.sub(
        r'(<script id="datos" type="application/json">)(.*?)(</script>)',
        lambda m: m.group(1) + "\n" + bloque + "\n" + m.group(3),
        plantilla, count=1, flags=re.S,
    )
    salida = RAIZ / "ejemplo" / "index.html"
    salida.write_text(html, encoding="utf-8")
    return salida


if __name__ == "__main__":
    print("Listo:", empacar())
    print("Listo:", ejemplo())
