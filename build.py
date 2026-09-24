#!/usr/bin/env python3
"""Construit la présentation : schémas SVG (figures.py) puis HTML reveal.js via pandoc.

Usage : python3 build.py   →   ouvre slides.html dans un navigateur
Touches utiles pendant la présentation : S (notes orateur), F (plein écran), Échap (vue d'ensemble).
"""

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# Chemin (relatif à ce dossier) ou URL de votre démo existante « réseau de neurones réglable ».
# Laisser vide : la slide affiche un encadré à la place.
DEMO_RESEAU = "demos/reseau.html?ni=2&nh=1&hs=2&no=1&act=step&t=OU"


def demo_block():
    if DEMO_RESEAU:
        return f'<iframe class="demo" data-src="{DEMO_RESEAU}"></iframe>'
    return ('<div class="demo-missing">Emplacement de votre démo « réseau de neurones réglable »<br>'
            '<small>renseigner <code>DEMO_RESEAU</code> dans <code>build.py</code></small></div>')


def main():
    subprocess.run(["python3", os.path.join(HERE, "figures.py")], check=True)
    with open(os.path.join(HERE, "slides.md"), encoding="utf-8") as f:
        md = f.read().replace("DEMO_RESEAU", demo_block(), 1)
    subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "revealjs", "-s", "--slide-level=2",
         "-o", os.path.join(HERE, "slides.html"),
         "-V", "revealjs-url=vendor/reveal.js",
         "-V", "theme=white",
         "-V", "width=1280", "-V", "height=720", "-V", "margin=0.04",
         "-V", "transition=fade", "-V", "slideNumber=true", "-V", "hash=true",
         "-V", "center=false",
         "--css", "theme.css"],
        input=md, text=True, check=True, cwd=HERE)
    print("→", os.path.join(HERE, "slides.html"))


if __name__ == "__main__":
    main()
