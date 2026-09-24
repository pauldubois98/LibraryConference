"""Mini-bibliothèque pour dessiner des diagrammes SVG homogènes (boîtes, flèches, texte)."""

from html import escape
import math

FONT = "Lato, 'Noto Sans', 'Helvetica Neue', Arial, sans-serif"

# Palette commune avec theme.css et demos/common.css
INK = "#1f2a44"
MUTED = "#6b7489"
LIGHT = "#eef1f6"
VIOLET = "#800080"      # couleur d'accent
VIOLET_L = "#f0d9f0"
ORANGE = "#ffc000"      # couleur principale (remplissages, traits)
ORANGE_D = "#b38600"    # même teinte, plus foncée : texte orange lisible sur fond blanc
ORANGE_L = "#fff2cc"
RED = "#c0392b"
RED_L = "#f7dcd8"
GREEN = "#2e8b57"
GREEN_L = "#d9f0e3"
BLUE = "#2e6fb3"        # couleur secondaire (biais, corpus…)
BLUE_L = "#dde8f5"
WHITE = "#ffffff"


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.items = []

    def raw(self, s):
        self.items.append(s)

    def text(self, x, y, s, fs=34, anchor="middle", color=INK, weight="normal",
             italic=False, lh=1.25):
        lines = str(s).split("\n")
        y0 = y - (len(lines) - 1) * fs * lh / 2
        style = "font-style:italic;" if italic else ""
        spans = "".join(
            f'<tspan x="{x}" y="{y0 + i * fs * lh:.1f}">{escape(l)}</tspan>'
            for i, l in enumerate(lines))
        self.raw(f'<text font-family="{FONT}" font-size="{fs}" fill="{color}" '
                 f'font-weight="{weight}" text-anchor="{anchor}" '
                 f'dominant-baseline="central" style="{style}">{spans}</text>')

    def rect(self, x, y, w, h, fill=LIGHT, stroke=None, sw=3, rx=18, dash=None, opacity=1):
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        da = f'stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="{fill}" {st} {da} opacity="{opacity}"/>')

    def box(self, x, y, w, h, s, fill=LIGHT, stroke=None, fs=32, color=INK,
            weight="normal", rx=18, sw=3, dash=None):
        """Boîte dont (x, y) est le coin supérieur gauche, texte centré."""
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash)
        self.text(x + w / 2, y + h / 2, s, fs, color=color, weight=weight)

    def cbox(self, cx, cy, w, h, s, **kw):
        """Boîte centrée sur (cx, cy)."""
        self.box(cx - w / 2, cy - h / 2, w, h, s, **kw)

    def circle(self, cx, cy, r, fill=LIGHT, stroke=None, sw=3):
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {st}/>')

    def line(self, x1, y1, x2, y2, color=MUTED, sw=4, dash=None, opacity=1):
        da = f'stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                 f'stroke-width="{sw}" stroke-linecap="round" {da} opacity="{opacity}"/>')

    def arrow(self, x1, y1, x2, y2, color=MUTED, sw=5, head=20, dash=None, opacity=1):
        ang = math.atan2(y2 - y1, x2 - x1)
        # la ligne s'arrête à la base de la pointe
        bx, by = x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang)
        self.line(x1, y1, bx, by, color, sw, dash, opacity)
        p1 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
        p2 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
        self.raw(f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" '
                 f'fill="{color}" opacity="{opacity}"/>')

    def curve_arrow(self, x1, y1, cx, cy, x2, y2, color=MUTED, sw=5, head=20):
        self.raw(f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{color}" '
                 f'stroke-width="{sw}" stroke-linecap="round"/>')
        ang = math.atan2(y2 - cy, x2 - cx)
        p1 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
        p2 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
        self.raw(f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" '
                 f'fill="{color}"/>')

    def save(self, path):
        body = "\n".join(self.items)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                    f'width="{self.w}" height="{self.h}">\n{body}\n</svg>\n')


def gear_path(cx, cy, r, teeth=10, depth=0.22):
    """Contour d'un engrenage (chemin SVG) centré sur (cx, cy)."""
    ri = r * (1 - depth)
    pts = []
    for k in range(teeth):
        a0 = 2 * math.pi * k / teeth
        step = 2 * math.pi / teeth
        for frac, rad in [(0.0, ri), (0.15, r), (0.45, r), (0.6, ri)]:
            a = a0 + frac * step
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def _gear(self, cx, cy, r, fill, teeth=10, spin=None, phase=0):
    """Engrenage avec moyeu ; spin = durée d'un tour en secondes (négatif = sens inverse),
    phase = rotation initiale des dents en degrés (pour que deux engrenages s'emboîtent)."""
    anim = ""
    if spin:
        end = -360 if spin < 0 else 360
        anim = (f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
                f'to="{end} {cx} {cy}" dur="{abs(spin)}s" repeatCount="indefinite"/>')
    rot = f'transform="rotate({phase} {cx} {cy})" ' if phase else ""
    self.raw(f'<g><path {rot}d="{gear_path(cx, cy, r, teeth)}" fill="{fill}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r * 0.28:.1f}" fill="#ffffff"/>{anim}</g>')


SVG.gear = _gear
