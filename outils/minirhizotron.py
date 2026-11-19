"""Schéma au trait d'un minirhizotron (viewBox 0 0 600 320).

Plant d'arachide au-dessus du sol (feuilles à quatre folioles, deux gynophores portant des gousses),
racine pivot et racines latérales ; tube transparent enfoncé à 45° qui dépasse du sol, bouchon en haut,
caméra à l'intérieur avec son câble ; cercle pointillé sur la fenêtre d'observation, et trait de
repère qui descend jusqu'au bas du dessin (il touche le cadre du premier panneau de la figure).
"""
import math
import random

SOL_Y = 110


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def feuille(x, y, angle):
    """Feuille d'arachide : rachis, deux paires de folioles obovales bien séparées."""
    ux, uy = math.cos(angle), math.sin(angle)
    nx, ny = -uy, ux
    bout = (x + 20 * ux, y + 20 * uy)
    out = [f'<path class="trait fin" d="M{f(x)} {f(y)} L{f(bout[0])} {f(bout[1])}"/>']
    for t in (0.5, 1.0):
        bx, by = x + 20 * t * ux, y + 20 * t * uy
        for s in (-1, 1):
            cx, cy = bx + s * 6 * nx + 1.5 * ux, by + s * 6 * ny + 1.5 * uy
            a = math.degrees(angle) + s * 62
            out.append(f'<ellipse class="trait" cx="{f(cx)}" cy="{f(cy)}" rx="5.6" ry="2.9" '
                       f'transform="rotate({f(a)} {f(cx)} {f(cy)})"/>')
    return out


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def gousse(x, y, angle):
    """Gousse d'arachide : deux lobes resserrés au milieu."""
    d = ("M-9 0 C-9 -4.5 -3 -5 -1 -3 C0 -2.4 1 -2.4 2 -3 C4 -5 9 -4.5 9 0 "
         "C9 4.5 4 5 2 3 C1 2.4 0 2.4 -1 3 C-3 5 -9 4.5 -9 0 Z")
    return f'<path class="trait" d="{d}" transform="translate({f(x)} {f(y)}) rotate({f(angle)})"/>'


# Tube : axe à 45°, du haut (au-dessus du sol) vers le bas à gauche ; demi-largeur 8
HAUT, BAS, R = (400, 70), (190, 280), 8
U = (-math.sqrt(0.5), math.sqrt(0.5))          # direction de l'axe, vers le bas du tube
N = (math.sqrt(0.5), math.sqrt(0.5))           # normale, vers la paroi inférieure


def pt(p, a=0, b=0):
    return (p[0] + a * U[0] + b * N[0], p[1] + a * U[1] + b * N[1])


CAMERA = (305, 165)
FENETRE = pt(CAMERA, 0, R + 0.5)                # point de la paroi inférieure vu par l'objectif
RAYON_REPERE = 15

lignes = []
ajout = lignes.append

# Sol : surface et quelques grains
ajout('<path class="trait" d="M10 110 C90 107 170 113 250 110 S410 107 590 111"/>')
random.seed(3)
grains = []
while len(grains) < 46:
    x, y = random.uniform(20, 580), random.uniform(SOL_Y + 10, 312)
    # pas de grain dans le tube ni trop près d'un autre
    proj = (x - HAUT[0]) * N[0] + (y - HAUT[1]) * N[1]
    if abs(proj) < R + 4 and y > SOL_Y:
        continue
    if all(math.dist((x, y), g) > 26 for g in grains):
        grains.append((x, y))
ajout('<g class="grains">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="1"/>' for x, y in grains) + "</g>")

# Plant d'arachide : plante basse et touffue, feuilles le long des tiges, gynophores et gousses
BASE = (250, 110)
tiges = [((240, 100), (214, 90), (180, 86)),
         ((238, 88), (222, 66), (204, 54)),
         ((248, 84), (246, 60), (240, 42)),
         ((256, 84), (266, 60), (282, 46)),
         ((262, 100), (288, 88), (322, 84))]
for c1, c2, bout in tiges:
    ajout(f'<path class="trait" d="M{BASE[0]} {BASE[1]} C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} '
          f'{f(bout[0])} {f(bout[1])}"/>')
    for i, t in enumerate((0.45, 0.75, 1.0)):
        x0, y0 = bezier(BASE, c1, c2, bout, t)
        xa, ya = bezier(BASE, c1, c2, bout, t - 0.03)
        tangente = math.atan2(y0 - ya, x0 - xa)
        ecart = 0 if t == 1.0 else (-1 if i % 2 == 0 else 1) * math.radians(42)
        lignes.extend(feuille(x0, y0, tangente + ecart))
ajout('<path class="trait fin" d="M243 104 C239 112 236 120 233 127"/>')
ajout(gousse(231, 131, 25).replace('rotate(25)', 'rotate(25) scale(0.8)'))
ajout('<path class="trait fin" d="M257 104 C262 112 266 120 268 127"/>')
ajout(gousse(270, 131, -20).replace('rotate(-20)', 'rotate(-20) scale(0.8)'))

# Racines : pivot et latérales qui partent à des hauteurs différentes ;
# l'une passe contre la fenêtre d'observation
racines = ["M250 110 C251 140 246 175 252 210 C257 245 250 280 254 320",
           "M251 128 C236 136 222 140 206 152 C194 161 186 172 176 178",
           "M206 152 C202 162 200 172 200 186",
           "M251 134 C266 142 282 144 296 152 C308 159 318 163 332 164",
           "M249 166 C232 173 216 187 206 205 C200 216 190 226 178 232",
           "M250 170 C268 167 292 167 311 172 C324 175 334 182 344 192",
           "M252 214 C236 226 222 244 214 268 C210 282 206 296 200 312",
           "M214 268 C224 276 232 286 236 300",
           "M253 222 C270 232 290 246 302 266 C310 280 318 292 330 306"]
for d in racines:
    ajout(f'<path class="trait racine" d="{d}"/>')

# Tube : parois, fond arrondi, bouchon
p1, p2 = pt(HAUT, 0, -R), pt(HAUT, 0, R)
q1, q2 = pt(BAS, 0, -R), pt(BAS, 0, R)
ajout(f'<path class="trait" d="M{f(p1[0])} {f(p1[1])} L{f(q1[0])} {f(q1[1])} '
      f'A{R} {R} 0 0 0 {f(q2[0])} {f(q2[1])} L{f(p2[0])} {f(p2[1])}"/>')
c1, c2 = pt(HAUT, -4, -R - 1), pt(HAUT, -4, R + 1)
b1, b2 = pt(HAUT, 0, -R - 1), pt(HAUT, 0, R + 1)
ajout(f'<path class="trait" d="M{f(b1[0])} {f(b1[1])} L{f(c1[0])} {f(c1[1])} L{f(c2[0])} {f(c2[1])} '
      f'L{f(b2[0])} {f(b2[1])} Z"/>')

# Caméra et câble
ajout(f'<rect class="trait" x="-14" y="-5" width="28" height="10" rx="2" '
      f'transform="translate({CAMERA[0]} {CAMERA[1]}) rotate(135)"/>')
ajout(f'<path class="trait" d="M-2 5 L4 5" transform="translate({CAMERA[0]} {CAMERA[1]}) rotate(135)" '
      f'stroke-width="2.5"/>')
haut_cam = pt(CAMERA, -14, 0)
sortie = pt(HAUT, -4, 0)
ajout(f'<path class="trait fin" d="M{f(haut_cam[0])} {f(haut_cam[1])} L{f(sortie[0])} {f(sortie[1])} '
      f'C{f(sortie[0] + 8)} {f(sortie[1] - 10)} 418 50 436 48"/>')

# Repère : cercle sur la fenêtre d'observation, trait jusqu'au bas du dessin
fx, fy = FENETRE
ajout(f'<g class="repere"><circle class="trait" cx="{f(fx)}" cy="{f(fy)}" r="{RAYON_REPERE}" '
      f'stroke-dasharray="3 3"/><path class="trait" d="M{f(fx)} {f(fy + RAYON_REPERE)} L{f(fx)} 320"/></g>')

print("\n".join(lignes))
