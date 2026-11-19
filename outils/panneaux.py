"""Panneaux de la Figure 1 (Root Segmentator), générés avec le modèle rootseg v1.1.

Pour chaque image d'exemple : image brute (recadrée comme le fait l'outil pour le capteur 120 DPI),
racines détectées (superposition produite par l'outil) et mesures (squelette du masque, c'est-à-dire
la ligne centrale qui sert à mesurer la longueur). Les valeurs sont formatées comme dans la démo.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

from prmi.inference import RootSegmentator, overlay
from prmi.preprocess import crop_for

EXEMPLES = Path("/home/francois/Bureau/e-portfolio/prmi-roots/examples/images")
CAS = [
    ("denses", "Racines denses", "Peanut_T019_L083_2016.06.13_130232_BAZ_DPI150"),
    ("fines", "Racines fines", "Peanut_T019_L046_2015.06.04_104607_BAZ_DPI150"),
    ("sombre", "Image sombre", "Peanut_T019_L077_2016.07.25_170233_BAZ_DPI150"),
    ("camera", "Autre caméra", "Peanut_T026_L049_2017.07.27_123345_EED_DPI120"),
    ("sans-racine", "Sans racine", "Peanut_T018_L064_2015.06.04_104218_BAZ_DPI150"),
]


def virgule(texte):
    return texte.replace(".", ",")


def panneau_mesures(image, masque):
    """Image assombrie, masque en bleu léger, squelette (ligne centrale mesurée) en blanc."""
    fond = np.clip(image, 0, 1).mean(axis=2, keepdims=True) * 0.5
    out = np.repeat(fond, 3, axis=2) * 255
    bleu = np.array((30, 100, 255), float)
    out[masque] = 0.7 * out[masque] + 0.3 * bleu
    squelette = ndi.binary_dilation(skeletonize(masque), iterations=1) if masque.any() else masque
    out[squelette] = (245, 245, 240)
    return out.astype(np.uint8)


def main(sortie):
    sortie = Path(sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    rs = RootSegmentator()
    valeurs = []
    for cle, libelle, nom in CAS:
        rgb = np.array(Image.open(EXEMPLES / f"{nom}.jpg").convert("RGB"))
        res = rs.analyze(rgb, name=nom)
        dpi = 120 if "DPI120" in nom else 150
        brute = rgb[crop_for(dpi)]
        panneaux = {"brute": brute, "detectees": overlay(res.image, res.masque),
                    "mesures": panneau_mesures(res.image, res.masque)}
        for p, tableau in panneaux.items():
            Image.fromarray(tableau).save(sortie / f"{cle}-{p}.webp", "WEBP", quality=80, method=6)
        m = res.mesures
        valeurs.append({
            "cle": cle, "libelle": libelle, "image": nom, "largeur": brute.shape[1], "hauteur": brute.shape[0],
            "longueur": virgule(f"{m['longueur_mm']:.1f}"),
            "diametre": virgule(f"{m['diametre_moyen_mm']:.2f}") if m["diametre_moyen_mm"] else None,
            "intensite": virgule(f"{m['intensite_mm_cm2']:.1f}"),
            "brut": {k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in m.items()},
        })
    print(json.dumps(valeurs, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
