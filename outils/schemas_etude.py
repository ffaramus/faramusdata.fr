"""Schémas SVG de la page détaillée de Root Segmentator.

Schéma 1 : le minirhizotron (dessin de l'accueil, sans trait de repère) avec quatre repères numérotés.
Schéma 2 : une même racine et son annotation en chaîne de rectangles, de quatre façons
(correcte, décalée, fendue, racine oubliée).
Écrit les fragments dans le dossier donné en argument.
"""
import math
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def schema_minirhizotron():
    dessin = subprocess.run([sys.executable, "-I", str(ICI / "minirhizotron.py"), "--sans-trait"],
                            capture_output=True, text=True, check=True).stdout.rstrip("\n")
    reperes = [(1, 372, 92), (2, 288, 150), (3, 334, 186), (4, 196, 214)]
    marques = "".join(
        f'<g class="marque"><circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y}">{n}</text></g>'
        for n, x, y in reperes)
    return dessin + "\n" + marques


def bezier(t, p0=(18, 34), p1=(70, 20), p2=(120, 120), p3=(186, 104)):
    u = 1 - t
    x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
    return x, y


def tangente(t):
    (x0, y0), (x1, y1) = bezier(max(t - 0.01, 0)), bezier(min(t + 0.01, 1))
    return math.degrees(math.atan2(y1 - y0, x1 - x0))


RACINE = "M18 34 C70 20 120 120 186 104"
BRANCHE = "M104 72 C112 92 116 108 114 132"


def rectangles(decalage=0.0, longueur=26, pas=24, debut=0.04, fin=0.96):
    """Chaîne de rectangles le long de la racine, orientés selon la tangente."""
    out, t = [], debut
    # pas approximatif en paramètre : la courbe fait environ 200 unités de long
    while t <= fin:
        x, y = bezier(t)
        a = tangente(t)
        nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
        cx, cy = x + decalage * nx, y + decalage * ny
        out.append(f'<rect class="annotation" x="{f(-longueur / 2)}" y="-6" width="{f(longueur)}" height="12" '
                   f'transform="translate({f(cx)} {f(cy)}) rotate({f(a)})"/>')
        t += pas / 200
    return "".join(out)


def schema_defauts():
    cas = {
        "correcte": rectangles(),
        "decalee": rectangles(decalage=13),
        "fendue": rectangles(longueur=13),
        "oubliee": rectangles(),
    }
    sorties = {}
    for cle, rects in cas.items():
        branche = f'<path class="racine" d="{BRANCHE}"/>' if cle == "oubliee" else ""
        sorties[cle] = f'<path class="racine" d="{RACINE}"/>{branche}{rects}'
    return sorties


if __name__ == "__main__":
    sortie = Path(sys.argv[1])
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "schema-minirhizotron.svg").write_text(schema_minirhizotron() + "\n", encoding="utf-8")
    for cle, contenu in schema_defauts().items():
        (sortie / f"defaut-{cle}.svg").write_text(contenu + "\n", encoding="utf-8")
    print("ok")
