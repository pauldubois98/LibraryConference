"""Génère tous les schémas de la présentation dans figures/ (SVG)."""

import os
import numpy as np
from svgkit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)


def out(name):
    return os.path.join(OUT, name)


# ---------------------------------------------------------------- info : coût
def info_balance():
    s = SVG(1600, 700)
    for k, (title, prod, verif) in enumerate([("Avant", 0.75, 0.55), ("Avec l'IA", 0.06, 0.55)]):
        x0 = 150 + k * 750
        s.text(x0 + 300, 60, title, fs=46, weight="bold", color=ORANGE_D if k == 0 else VIOLET)
        for j, (lab, v, c) in enumerate([("Produire\nun contenu", prod, VIOLET),
                                         ("Vérifier\nun contenu", verif, ORANGE)]):
            x = x0 + 60 + j * 280
            H = 460
            s.rect(x, 130, 180, H, fill=LIGHT, rx=12)
            s.rect(x, 130 + H * (1 - v), 180, H * v, fill=c, rx=12)
            s.text(x + 90, 650, lab, fs=30)
        s.text(x0 + 300, 105, "", fs=20)
    s.text(120, 360, "coût", fs=28, color=MUTED, anchor="end", italic=True)
    s.save(out("info_cout.svg"))


# ---------------------------------------------------------------- système expert
def expert_system():
    s = SVG(1150, 780)
    B, N = dict(fill=ORANGE_L, stroke=ORANGE, fs=30), dict(fs=26, weight="bold")

    def yes(x1, y1, x2, y2):
        s.arrow(x1, y1, x2, y2, sw=4, head=16); s.text((x1 + x2) / 2 - 45, (y1 + y2) / 2 - 5, "oui", color=GREEN, **N)

    def no(x1, y1, x2, y2):
        s.arrow(x1, y1, x2, y2, sw=4, head=16); s.text((x1 + x2) / 2 + 45, (y1 + y2) / 2 - 5, "non", color=RED, **N)

    def leaf(cx, cy, t):
        s.cbox(cx, cy, 210, 80, t, fill=GREEN_L, stroke=GREEN, fs=30, weight="bold")

    s.cbox(575, 45, 380, 70, "Une zone de l'image", fill=LIGHT, fs=30, weight="bold")
    s.arrow(575, 82, 575, 130, sw=4, head=16)
    s.cbox(575, 175, 300, 80, "Plutôt bleu ?", **B)
    yes(480, 217, 300, 290); no(670, 217, 850, 290)
    s.cbox(270, 330, 340, 80, "En haut de l'image ?", **B)
    s.cbox(870, 330, 290, 80, "Plutôt blanc ?", **B)
    yes(200, 372, 140, 440); no(340, 372, 400, 440)
    leaf(130, 485, "ALORS ciel"); leaf(410, 485, "ALORS mer")
    yes(800, 372, 700, 440); no(940, 372, 990, 440)
    leaf(680, 485, "ALORS nuage")
    s.cbox(990, 485, 270, 80, "Plutôt vert ?", **B)
    yes(930, 527, 860, 590); no(1050, 527, 1080, 590)
    leaf(850, 635, "ALORS herbe")
    s.cbox(1060, 635, 170, 80, "…", fill=LIGHT, stroke=MUTED, fs=36, dash="8 6")
    s.text(300, 700, "Règles écrites par des humains", fs=34, color=ORANGE_D, weight="bold")
    s.save(out("systeme_expert.svg"))


def cats_ml():
    s = SVG(1600, 640)
    ex = [("🐱", "chat", GREEN), ("🐶", "pas chat", RED), ("🐈", "chat", GREEN),
          ("🦁", "pas chat", RED), ("🐈‍⬛", "chat", GREEN), ("🐰", "pas chat", RED)]
    for i, (e, lab, c) in enumerate(ex):
        x = 90 + (i % 2) * 230
        y = 30 + (i // 2) * 180
        s.rect(x, y, 200, 170, fill=WHITE, stroke=c, sw=4)
        s.text(x + 100, y + 70, e, fs=80)
        s.text(x + 100, y + 145, lab, fs=26, color=c, weight="bold")
    s.text(320, 600, "des milliers d'exemples étiquetés", fs=28, color=MUTED, italic=True)
    s.arrow(590, 300, 760, 300, sw=7)
    s.gear(920, 270, 125, VIOLET, teeth=12, spin=12)
    # vitesses dans le rapport des dents (12/8) et petit engrenage décalé pour que les dents s'emboîtent
    s.gear(1060, 395, 75, ORANGE, teeth=8, spin=-8, phase=10)
    s.text(960, 540, "entraînement", fs=38, color=VIOLET, weight="bold")
    s.arrow(1150, 300, 1260, 300, sw=7)
    s.rect(1280, 170, 260, 260, fill=WHITE, stroke=MUTED, sw=4, dash="12 10")
    s.text(1410, 270, "🐈", fs=110)
    s.text(1410, 380, "chat : 97 %", fs=32, color=GREEN, weight="bold")
    s.text(1410, 480, "nouvelle image", fs=28, color=MUTED, italic=True)
    s.save(out("chat_ml.svg"))


def neuron():
    s = SVG(1600, 720)
    xs = [(150, 190), (150, 360), (150, 530)]
    sx, sy, sr = 760, 360, 105
    heads = [(150, "entrées"), (430, "poids"), (sx, "somme"), (1130, "activation"), (1460, "sortie")]
    for x, t in heads:
        s.text(x, 50, t, fs=30, color=MUTED, italic=True)
    for k, (x, y) in enumerate(xs):
        s.line(x + 55, y, sx - sr + 5, sy, color=[ORANGE, RED, ORANGE][k], sw=[7, 4, 10][k])
        mx, my = x + (sx - x) * 0.42, y + (sy - y) * 0.42
        s.cbox(mx, my, 90, 52, f"w{'₁₂₃'[k]}", fill=WHITE, stroke=[ORANGE, RED, ORANGE][k], fs=30, rx=26)
        s.circle(x, y, 55, fill=LIGHT, stroke=INK)
        s.text(x, y, f"x{'₁₂₃'[k]}", fs=40)
    # biais
    s.cbox(sx, 120, 170, 64, "b", fill=BLUE_L, stroke=BLUE, fs=28, rx=32)
    s.arrow(sx, 152, sx, sy - sr - 4, color=BLUE, sw=4, head=16)
    s.circle(sx, sy, sr, fill=VIOLET_L, stroke=VIOLET, sw=5)
    s.text(sx, sy - 12, "Σ", fs=80, color=VIOLET, weight="bold")
    s.arrow(sx + sr + 5, sy, 1010, sy, sw=6, head=22)
    # fonction d'activation (sigmoïde)
    bx, by, bw, bh = 1020, 260, 220, 200
    s.rect(bx, by, bw, bh, fill=WHITE, stroke=ORANGE, sw=5)
    s.line(bx + 15, by + bh / 2, bx + bw - 15, by + bh / 2, color="#d0d5de", sw=2)
    s.line(bx + bw / 2, by + 15, bx + bw / 2, by + bh - 15, color="#d0d5de", sw=2)
    pts = []
    for k in range(61):
        t = -6 + 12 * k / 60
        pts.append((bx + 15 + (bw - 30) * k / 60, by + bh - 25 - (bh - 50) / (1 + np.exp(-t))))
    s.raw('<polyline fill="none" stroke="%s" stroke-width="6" stroke-linecap="round" points="%s"/>'
          % (ORANGE, " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    s.text(bx + bw / 2, by + bh + 40, "f", fs=36, color=ORANGE_D, weight="bold", italic=True)
    s.arrow(bx + bw + 5, sy, 1390, sy, sw=6, head=22)
    s.circle(1460, sy, 65, fill=ORANGE, stroke=None)
    s.text(1460, sy, "y", fs=46, color=INK, weight="bold")
    s.raw(f'<text x="800" y="650" font-family="{FONT}" font-size="44" fill="{INK}" text-anchor="middle">'
          f'y = <tspan fill="{ORANGE_D}" font-style="italic" font-weight="bold">f</tspan>( '
          f'<tspan fill="{ORANGE_D}">w₁</tspan>·x₁ + <tspan fill="{RED}">w₂</tspan>·x₂ + '
          f'<tspan fill="{ORANGE_D}">w₃</tspan>·x₃ + <tspan fill="{BLUE}">b</tspan> )</text>')
    s.save(out("neurone.svg"))


# ---------------------------------------------------------------- réseau de neurones


def scale_params():
    s = SVG(1600, 700)
    data = [("Réseau de\ndémonstration", 10, "~10"), ("Reconnaître des\nchiffres (1998)", 6e4, "60 000"),
            ("GPT-2\n(2019)", 1.5e9, "1,5 milliard"), ("GPT-3\n(2020)", 1.75e11, "175 milliards"),
            ("Grands modèles\nactuels", 1e12, "~1 000 milliards ?")]
    base_y, top = 560, 90
    lmax = 12.5
    for i, (lab, v, txt) in enumerate(data):
        x = 130 + i * 290
        h = (base_y - top) * max(np.log10(v), 0.3) / lmax
        col = VIOLET if i == len(data) - 1 else ORANGE
        s.rect(x, base_y - h, 190, h, fill=col, rx=10)
        s.text(x + 95, base_y - h - 35, txt, fs=30, weight="bold", color=ORANGE_D if col == ORANGE else col)
        s.text(x + 95, base_y + 60, lab, fs=26)
    s.line(90, base_y, 1560, base_y, color=INK, sw=3)
    s.save(out("echelle_parametres.svg"))


# ---------------------------------------------------------------- entraînement
def training_loop():
    s = SVG(1600, 780)
    cx, cy, rx, ry = 800, 400, 434, 280
    steps = [("Exemple\n(donnée)", LIGHT, INK), ("Prédiction\ndu modèle", VIOLET_L, INK),
             ("Comparaison avec\nla bonne réponse", ORANGE_L, INK), ("Erreur", RED_L, RED),
             ("On ajuste\nles parametres", GREEN_L, GREEN)]
    n, bw, bh = len(steps), 330, 120
    angles = [-np.pi / 2 + 2 * np.pi * i / n for i in range(n)]
    pts = [(cx + rx * np.cos(a), cy + ry * np.sin(a)) for a in angles]

    def outside(x, y, box, margin=14):
        return abs(x - box[0]) > bw / 2 + margin or abs(y - box[1]) > bh / 2 + margin

    # flèches : arcs de l'ellipse entre le bord d'une boîte et le bord de la suivante
    for i in range(n):
        ts = np.linspace(angles[i], angles[i] + 2 * np.pi / n, 200)
        arc = [(cx + rx * np.cos(t), cy + ry * np.sin(t)) for t in ts]
        arc = [p for p in arc if outside(*p, pts[i]) and outside(*p, pts[(i + 1) % n])]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in arc[:-6])
        s.raw(f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="5" stroke-linecap="round"/>')
        s.arrow(*arc[-7], *arc[-1], color=MUTED, sw=5, head=22)
    for (x, y), (lab, fill, col) in zip(pts, steps):
        s.cbox(x, y, bw, bh, lab, fill=fill, fs=30, color=col, weight="bold")
    s.text(cx, cy - 20, "× des millions de fois", fs=44, weight="bold", color=ORANGE_D)
    s.save(out("boucle_entrainement.svg"))


def tokens_split():
    s = SVG(1600, 640)
    phrase = "La bibliothèque ouvre à 9h."
    rows = [("Caractères", list(phrase), LIGHT, 42),
            ("Mots", ["La", "bibliothèque", "ouvre", "à", "9h", "."], ORANGE_L, None),
            ("Tokens", ["La", " biblio", "thèque", " ouvre", " à", " 9", "h", "."], VIOLET_L, None)]
    x_start, x_end = 260, 1420
    for r, (lab, units, col, fixed_w) in enumerate(rows):
        y = 50 + r * 150
        s.text(x_start - 30, y + 45, lab, fs=36, anchor="end", weight="bold")
        n = len(units)
        gap = 6 if fixed_w else 12
        # largeur proportionnelle au nombre de caractères
        lens = [max(len(u), 1) for u in units]
        avail = x_end - x_start - gap * (n - 1)
        x = x_start
        for u, L in zip(units, lens):
            w = avail * L / sum(lens)
            s.box(x, y, w, 90, u.replace(" ", "␣"), fill=col, fs=34 if not fixed_w else 30, rx=10)
            x += w + gap
        s.text(1540, y + 45, str(n), fs=44, weight="bold", color=[MUTED, ORANGE_D, VIOLET][r])
    s.text(1540, 20, "unités", fs=24, color=MUTED)
    notes = [("Caractères", "peu de symboles, mais des séquences très longues", MUTED),
             ("Mots", "séquences courtes, mais vocabulaire infini (noms, fautes, néologismes…)", ORANGE_D),
             ("Tokens", "le compromis : des morceaux fréquents, ~50 000 à 200 000 au total", VIOLET)]
    for i, (a, b, c) in enumerate(notes):
        y = 510 + i * 44
        s.text(260, y, a + " :", fs=28, anchor="end", weight="bold", color=c)
        s.text(280, y, b, fs=28, anchor="start", color=INK)
    s.save(out("tokens.svg"))


def letters_nn():
    """Réseau qui lit 3 lettres (un neurone par lettre possible) et prédit la suivante."""
    s = SVG(1600, 830)
    letters = ["a", "b", "c", "d", "e", "h", "i", "m", "n", "r", "s", "t", "…", "z"]
    word = ["c", "h", "a"]
    out_act = {"t": 0.62, "r": 0.15, "n": 0.09, "m": 0.06, "s": 0.04}
    top, gap, r = 150, 45, 17
    ys = [top + k * gap for k in range(len(letters))]
    in_x = [150, 330, 510]
    hid_x, hid_y = 900, [top + 90 + k * 95 for k in range(6)]
    out_x = 1260

    # connexions : seules celles des neurones actifs sont appuyées
    for k, x in enumerate(in_x):
        for i, l in enumerate(letters):
            if l == "…":
                continue
            on = l == word[k]
            for hy in hid_y:
                s.line(x + r, ys[i], hid_x - 30, hy, color=VIOLET if on else "#dfe3ea",
                       sw=2.5 if on else 1, opacity=0.9 if on else 0.6)
    for hy in hid_y:
        for i, l in enumerate(letters):
            if l == "…":
                continue
            best = l == "t"
            s.line(hid_x + 30, hy, out_x - r, ys[i], color=ORANGE if best else "#dfe3ea",
                   sw=2.5 if best else 1, opacity=0.9 if best else 0.6)

    # entrées : 3 colonnes, un neurone par lettre (fond blanc : les traits passent « sous » les colonnes)
    for x in in_x:
        s.rect(x - 55, ys[0] - 25, 80, ys[-1] - ys[0] + 50, fill=WHITE, rx=10, opacity=0.92)
    for k, x in enumerate(in_x):
        s.text(x, 60, f"{k + 1}{'re' if k == 0 else 'e'} lettre", fs=28, color=MUTED)
        s.cbox(x, 108, 70, 56, word[k], fill=VIOLET, color=WHITE, fs=36, weight="bold", rx=12)
        for i, l in enumerate(letters):
            if l == "…":
                s.text(x, ys[i], "⋮", fs=30, color=MUTED)
                continue
            on = l == word[k]
            s.circle(x, ys[i], r, fill=VIOLET if on else WHITE, stroke=VIOLET if on else "#b8bfcc", sw=2)
            s.text(x - 40, ys[i], l, fs=24, color=VIOLET if on else MUTED, weight="bold" if on else "normal")
            if on:
                s.text(x, ys[i], "1", fs=20, color=WHITE, weight="bold")
    # couche cachée
    s.text(hid_x, 60, "couche cachée", fs=28, color=MUTED)
    for hy in hid_y:
        s.circle(hid_x, hy, 30, fill=ORANGE_L, stroke=ORANGE, sw=3)
    # sorties : une par lettre, intensité = activation
    s.text(out_x + 90, 60, "lettre suivante", fs=28, color=MUTED)
    for i, l in enumerate(letters):
        if l == "…":
            s.text(out_x, ys[i], "⋮", fs=30, color=MUTED)
            continue
        a = out_act.get(l, 0.01)
        best = l == "t"
        s.circle(out_x, ys[i], r, fill=ORANGE if best else (ORANGE_L if a > 0.02 else WHITE),
                 stroke=ORANGE if a > 0.02 else "#b8bfcc", sw=2)
        s.text(out_x + 40, ys[i], l, fs=24, color=ORANGE_D if best else MUTED, weight="bold" if best else "normal")
        s.rect(out_x + 65, ys[i] - 12, max(3, 220 * a), 24, fill=ORANGE if best else "#ffe699", rx=5)
        if a > 0.02:
            s.text(out_x + 75 + 220 * a, ys[i], f"{round(100 * a)} %", fs=22, anchor="start",
                   color=ORANGE_D if best else MUTED, weight="bold" if best else "normal")
    s.cbox(out_x + 90, 108, 150, 56, "t", fill=ORANGE, color=INK, fs=36, weight="bold", rx=12)
    s.text(800, 800, "« c h a »  →  le neurone le plus activé : « t »  →  « chat »", fs=32, color=INK, weight="bold")
    s.save(out("lettres.svg"))


def softmax_T(logits, T):
    z = np.array(logits) / T
    z -= z.max()
    p = np.exp(z)
    return p / p.sum()


def temperature_static():
    toks = ["France", "Europe", "Paris", "l'Île", "Seine", "plein", "effet", "zone"]
    probs0 = np.array([0.80, 0.08, 0.04, 0.03, 0.02, 0.015, 0.01, 0.005])
    logits = np.log(probs0)
    s = SVG(1600, 700)
    s.text(800, 40, "« Paris est situé en … »", fs=40, italic=True, color=MUTED)
    for k, (T, lab) in enumerate([(0.3, "Température basse (0,3)"), (1.0, "Normale (1)"), (2.5, "Élevée (2,5)")]):
        p = softmax_T(logits, T)
        x0 = 40 + k * 520
        s.text(x0 + 250, 110, lab, fs=32, weight="bold", color=[ORANGE_D, INK, VIOLET][k])
        for i, t in enumerate(toks):
            y = 160 + i * 64
            s.text(x0 + 140, y + 22, t, fs=30, anchor="end")
            s.rect(x0 + 155, y, 300 * p[i] + 2, 48, fill=[ORANGE, MUTED, VIOLET][k], rx=6)
            s.text(x0 + 165 + 300 * p[i], y + 22, f"{100 * p[i]:.0f}%", fs=26, anchor="start", color=MUTED)
    s.save(out("temperature.svg"))


def chat_as_text():
    s = SVG(1600, 700)
    s.text(380, 40, "Interface utilisateur", fs=36, weight="bold", color=ORANGE_D)
    s.box(80, 90, 520, 90, "Bonjour ! Un roman pour l'été ?", fill=ORANGE_L, fs=28)
    s.box(200, 200, 520, 130, "Volontiers : aimez-vous plutôt\nles policiers ou les sagas ?", fill=LIGHT, fs=28)
    s.box(80, 350, 520, 90, "Plutôt les policiers.", fill=ORANGE_L, fs=28)
    s.box(200, 460, 520, 90, "…", fill=LIGHT, fs=40)
    s.arrow(760, 330, 860, 330, sw=8, head=28)
    s.text(1210, 40, "Point de vu du LLM", fs=36, weight="bold", color=VIOLET)
    s.rect(880, 80, 660, 520, fill=WHITE, stroke=VIOLET, sw=4)
    lines = [("Conversation utilisateur / assistant bienveillant.", MUTED),
             ("Utilisateur : Bonjour ! Un roman pour l'été ?", INK),
             ("Assistant : Volontiers : aimez-vous plutôt", INK),
             ("   les policiers ou les sagas ?", INK),
             ("Utilisateur : Plutôt les policiers.", INK),
             ("Assistant :", VIOLET)]
    for i, (l, c) in enumerate(lines):
        s.text(910, 130 + i * 62, l, fs=26, anchor="start", color=c, weight="bold" if c == VIOLET else "normal")
    s.rect(1040, 420, 36, 44, fill=VIOLET, rx=4, opacity=0.6)
    s.save(out("conversation.svg"))


# ---------------------------------------------------------------- biais
def mini_net(s, x0, y0, hot_weights=False):
    """Petit réseau (3 → 3 → 2) dessiné dans un cadre 360×260 dont (x0, y0) est le coin haut-gauche."""
    L = [[(x0 + 50, y0 + 50 + i * 80) for i in range(3)],
         [(x0 + 180, y0 + 50 + i * 80) for i in range(3)],
         [(x0 + 310, y0 + 90 + i * 80) for i in range(2)]]
    hot = {(0, 0, 1), (0, 2, 1), (1, 1, 0), (1, 1, 1), (0, 1, 2)}
    for l in range(2):
        for i, (ax, ay) in enumerate(L[l]):
            for j, (bx, by) in enumerate(L[l + 1]):
                h = hot_weights and (l, i, j) in hot
                s.line(ax, ay, bx, by, color=RED if h else MUTED, sw=9 if h else 3, opacity=1 if h else 0.6)
    for layer in L:
        for (cx, cy) in layer:
            s.circle(cx, cy, 22, fill=WHITE, stroke=INK, sw=3)


def two_biases():
    s = SVG(1600, 720)
    for k, title in enumerate(["Biais dans le modèle", "Biais dans l'instruction / l'usage"]):
        x0 = 40 + k * 800
        on_model, on_instr = k == 0, k == 1
        s.text(x0 + 360, 45, title, fs=40, weight="bold", color=[ORANGE_D, VIOLET][k])
        # instruction
        s.box(x0 + 30, 130, 660, 100, "Instruction : « Résume ce débat »",
              fill=RED_L if on_instr else LIGHT, stroke=RED if on_instr else None, sw=5, fs=30,
              weight="bold" if on_instr else "normal")
        s.arrow(x0 + 360, 235, x0 + 360, 290)
        # modèle
        s.rect(x0 + 160, 300, 400, 280, fill=RED_L if on_model else LIGHT, stroke=RED if on_model else None, sw=5)
        mini_net(s, x0 + 180, 310, hot_weights=on_model)
        s.arrow(x0 + 360, 585, x0 + 360, 630)
        s.box(x0 + 210, 640, 300, 70, "Réponse", fill=WHITE, stroke=MUTED, fs=30)
        if on_model:
            s.text(x0 + 80, 440, "les\npoids", fs=30, color=RED, weight="bold")
    s.line(800, 70, 800, 700, color=LIGHT, sw=6)
    s.save(out("deux_biais.svg"))


def training_bias():
    s = SVG(1600, 720)
    s.text(420, 40, "Textes d'entrainement", fs=36, weight="bold", color=ORANGE_D)
    corpora = [("Pages web", True), ("Livres", True), ("Wikipédia", True), ("Code informatique", True),
               ("Forums", False), ("Presse", True), ("Textes en d'autres langues", False)]
    for i, (c, keep) in enumerate(corpora):
        y = 80 + i * 82
        s.box(120, y, 480, 66, c, fill=GREEN_L if keep else RED_L, fs=28,
              color=INK if keep else MUTED)
        s.text(650, y + 33, "✓" if keep else "✗", fs=44, weight="bold", color=GREEN if keep else RED)
        if not keep:
            s.line(150, y + 33, 570, y + 33, color=RED, sw=4)
    s.text(1130, 40, "Poid associé", fs=36, weight="bold", color=VIOLET)
    mix = [("Pages web", 0.45, ORANGE), ("Livres", 0.15, VIOLET), ("Wikipédia", 0.08, BLUE),
           ("Code", 0.17, GREEN), ("Presse", 0.15, RED)]
    x, W = 800, 660
    for name, p, c in mix:
        s.rect(x, 110, W * p, 120, fill=c, rx=4)
        x += W * p
    for i, (name, p, c) in enumerate(mix):
        y = 280 + i * 50
        s.rect(830, y - 16, 32, 32, fill=c, rx=6)
        s.text(880, y, f"{name} : {round(100 * p)} %", fs=28, anchor="start")
    s.text(1130, 560, "(proportions illustratives)", fs=24, color=MUTED, italic=True)
    s.save(out("biais_entrainement.svg"))


def usage_bias():
    s = SVG(1600, 700)
    s.rect(40, 40, 720, 420, fill=VIOLET_L, stroke=VIOLET, sw=4, dash="14 10")
    s.text(400, 85, "Instructions ajoutées (souvent invisibles)", fs=30, weight="bold", color=VIOLET)
    rules = ["« N'explique pas comment fabriquer une bombe. »",
             "« Ne fais la promotion d'aucun parti politique. »",
             "« Reste poli et nuancé. »"]
    for i, r in enumerate(rules):
        s.box(70, 130 + i * 105, 660, 85, r, fill=WHITE, fs=26)
    s.box(40, 510, 720, 110, "Question de l'utilisateur", fill=LIGHT, fs=32, weight="bold")
    s.arrow(770, 250, 930, 340, sw=5, color=VIOLET)
    s.arrow(770, 565, 930, 400, sw=5)
    s.cbox(1060, 370, 240, 180, "IA", fill=ORANGE, color=INK, fs=40, weight="bold")
    s.arrow(1185, 370, 1300, 370, sw=5)
    s.cbox(1430, 370, 240, 150, "Réponse", fill=WHITE, stroke=MUTED, fs=34)
    s.save(out("biais_usage.svg"))


# ---------------------------------------------------------------- humain
def better_vs_preferred():
    s = SVG(1600, 680)
    rows = [("Musée", "📱", "Tablette", "plus d'informations", "🧑‍🏫", "Visite guidée", "on préfère souvent"),
            ("Musique", "🎧", "MP3", "plus pratique, parfait", "🎤", "Concert", "on y va quand même")]
    s.text(560, 40, "« objectivement meilleur »", fs=34, color=ORANGE_D, weight="bold")
    s.text(1200, 40, "« socialement préféré »", fs=34, color=VIOLET, weight="bold")
    for i, (dom, e1, t1, d1, e2, t2, d2) in enumerate(rows):
        y = 100 + i * 280
        s.text(130, y + 110, dom, fs=40, weight="bold")
        s.box(300, y, 520, 220, "", fill=ORANGE_L)
        s.text(400, y + 110, e1, fs=100)
        s.text(640, y + 85, t1, fs=38, weight="bold")
        s.text(640, y + 145, d1, fs=26, color=MUTED)
        # s.text(880, y + 110, "≠", fs=80, color=INK, weight="bold")
        s.box(940, y, 520, 220, "", fill=VIOLET_L)
        s.text(1040, y + 110, e2, fs=100)
        s.text(1280, y + 85, t2, fs=38, weight="bold")
        s.text(1280, y + 145, d2, fs=26, color=MUTED)
    s.save(out("meilleur_vs_prefere.svg"))


# ---------------------------------------------------------------- manipulation
def fake_media():
    s = SVG(1600, 380)
    items = [("📝", "Texte"), ("🖼️", "Images"), ("🎬", "Vidéos"), ("🎙️", "Voix"), ("👥", "Faux comptes")]
    for i, (e, t) in enumerate(items):
        x = 110 + i * 290
        s.box(x, 40, 240, 260, "", fill=RED_L)
        s.text(x + 120, 140, e, fs=110)
        s.text(x + 120, 250, t, fs=32, weight="bold")
    s.save(out("fake_medias.svg"))


def chatbot_vs_agent():
    s = SVG(1600, 760)
    s.text(330, 40, "Chatbot", fs=42, weight="bold", color=ORANGE_D)
    s.cbox(330, 150, 300, 100, "Utilisateur", fill=LIGHT, fs=32)
    s.arrow(330, 205, 330, 285)
    s.cbox(330, 350, 260, 110, "LLM", fill=ORANGE, color=INK, fs=40, weight="bold")
    s.arrow(330, 410, 330, 490)
    s.cbox(330, 560, 300, 110, "📝 Texte", fill=ORANGE_L, fs=34)
    s.text(330, 690, "reste dans le monde du texte", fs=28, color=MUTED, italic=True)
    s.line(680, 40, 680, 720, color=LIGHT, sw=6)
    s.text(1140, 40, "Agent", fs=42, weight="bold", color=VIOLET)
    s.cbox(1140, 150, 300, 100, "Utilisateur", fill=LIGHT, fs=32)
    s.arrow(1140, 205, 1140, 285)
    s.cbox(1140, 350, 260, 110, "LLM", fill=VIOLET, color=WHITE, fs=40, weight="bold")
    tools = [("🌐", "Web"), ("📁", "Fichiers"), ("⌨️", "Terminal"), ("✉️", "E-mail")]
    for i, (e, t) in enumerate(tools):
        x = 810 + i * 220
        s.arrow(1140, 410, x, 500, sw=4)
        s.cbox(x, 570, 190, 130, "", fill=VIOLET_L)
        s.text(x, 545, e, fs=50)
        s.text(x, 605, t, fs=28, weight="bold")
    s.text(1140, 700, "chaque sortie peut déclencher une action", fs=28, color=RED, italic=True, weight="bold")
    s.save(out("chatbot_vs_agent.svg"))


def hf_incident():
    s = SVG(1600, 620)
    steps = [("Test interne\nd'OpenAI", LIGHT), ("L'IA sort de son\nbac à sable", VIOLET_L),
             ("Elle pirate\nHugging Face", RED_L), ("Repérée", GREEN_L)]
    w, gap = 320, 60
    x0 = (1600 - (4 * w + 3 * gap)) / 2
    s.text(800, 40, "juillet 2026", fs=32, color=MUTED, weight="bold")
    for i, (t, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        s.box(x, 90, w, 160, t, fill=c, fs=36, weight="bold")
        if i < 3:
            s.arrow(x + w + 6, 170, x + w + gap - 6, 170, sw=6, head=20)
    s.rect(250, 340, 1100, 200, fill=WHITE, stroke=VIOLET, sw=5)
    s.text(800, 400, "Son but : réussir le test", fs=40, weight="bold")
    s.text(800, 475, "… en allant voler les réponses", fs=40, weight="bold", color=RED)
    s.save(out("incident_hf.svg"))


def jakesch():
    s = SVG(1600, 720)
    s.cbox(190, 410, 300, 180, "1 506\nparticipants", fill=LIGHT, fs=36, weight="bold")
    s.text(800, 45, "Écrire un texte : « les réseaux sociaux sont-ils bons pour la société ? »", fs=30, italic=True)
    groups = [("Écrit seul", "(groupe témoin)", LIGHT, INK),
              ("Avec une IA réglée\nsur « plutôt POUR »", "", ORANGE_L, INK),
              ("Avec une IA réglée\nsur « plutôt CONTRE »", "", VIOLET_L, INK)]
    for i, (t, sub, c, col) in enumerate(groups):
        y = 150 + i * 190
        s.arrow(345, 410, 520, y + 70, sw=4)
        s.box(530, y, 460, 140, t + ("\n" + sub if sub else ""), fill=c, fs=28, weight="bold" if i else "normal")
        s.arrow(1000, y + 70, 1090, y + 70, sw=4)
    s.box(1100, 150, 440, 140, "Référence", fill=LIGHT, fs=30)
    s.box(1100, 340, 440, 140, "Textes plus « pour »\n+ opinion déplacée", fill=ORANGE, color=INK, fs=28, weight="bold")
    s.box(1100, 530, 440, 140, "Textes plus « contre »\n+ opinion déplacée", fill=VIOLET, color=WHITE, fs=28, weight="bold")
    s.save(out("jakesch.svg"))


if __name__ == "__main__":
    info_balance()
    expert_system()
    cats_ml()
    neuron()
    scale_params()
    training_loop()
    letters_nn()
    tokens_split()
    temperature_static()
    chat_as_text()
    two_biases()
    training_bias()
    usage_bias()
    better_vs_preferred()
    fake_media()
    chatbot_vs_agent()
    hf_incident()
    jakesch()
    print("figures générées dans", OUT)
