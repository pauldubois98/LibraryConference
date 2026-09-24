#!/usr/bin/env python3
"""Construit la présentation : schémas SVG (figures.py) puis HTML reveal.js via pandoc.

Usage : python3 build.py   →   ouvre slides.html dans un navigateur
Touches utiles pendant la présentation : S (notes orateur), F (plein écran), Échap (vue d'ensemble).
"""

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    subprocess.run(["python3", os.path.join(HERE, "figures.py")], check=True)
    with open(os.path.join(HERE, "slides.md"), encoding="utf-8") as f:
        md = f.read()
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
