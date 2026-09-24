"""Génère tous les schémas de la présentation dans figures/ (SVG)."""

import os
import numpy as np
from svgkit import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)


def out(name):
    return os.path.join(OUT, name)


# ---------------------------------------------------------------- fil conducteur
ROADMAP = ["Comment\nça marche ?", "Pourquoi ça\nfonctionne ?", "Quels\nbiais ?",
           "Quels\nusages ?", "Quels risques pour\nla démocratie ?"]


def roadmap(active=None, name="roadmap.svg"):
    s = SVG(1600, 360)
    n = len(ROADMAP)
    w, h, gap = 260, 170, 60
    x0 = (1600 - (n * w + (n - 1) * gap)) / 2
    for i, lab in enumerate(ROADMAP):
        x = x0 + i * (w + gap)
        on = active is None or active == i
        fill = TEAL if (active == i) else (TEAL_L if on else LIGHT)
        col = WHITE if active == i else (INK if on else MUTED)
        s.box(x, 95, w, h, lab, fill=fill, fs=30, color=col, weight="bold")
        s.text(x + w / 2, 45, str(i + 1), fs=34, color=TEAL if on else MUTED, weight="bold")
        if i < n - 1:
            s.arrow(x + w + 8, 180, x + w + gap - 8, 180, color=MUTED)
    s.save(out(name))


# ---------------------------------------------------------------- info : coût
def info_balance():
    s = SVG(1600, 700)
    for k, (title, prod, verif) in enumerate([("Avant", 0.75, 0.55), ("Avec l'IA", 0.06, 0.55)]):
        x0 = 150 + k * 750
        s.text(x0 + 300, 60, title, fs=46, weight="bold", color=TEAL if k == 0 else ORANGE)
        for j, (lab, v, c) in enumerate([("Produire\nun contenu", prod, ORANGE),
                                         ("Vérifier\nun contenu", verif, TEAL)]):
            x = x0 + 60 + j * 280
            H = 460
            s.rect(x, 130, 180, H, fill=LIGHT, rx=12)
            s.rect(x, 130 + H * (1 - v), 180, H * v, fill=c, rx=12)
            s.text(x + 90, 650, lab, fs=30)
        s.text(x0 + 300, 105, "", fs=20)
    s.text(1540, 360, "coût", fs=28, color=MUTED, anchor="end", italic=True)
    s.save(out("info_cout.svg"))


# ---------------------------------------------------------------- système expert
def expert_system():
    s = SVG(1600, 760)
    s.cbox(800, 70, 560, 90, "Une image arrive", fill=LIGHT, fs=34, weight="bold")
    s.arrow(800, 115, 800, 175)
    s.cbox(800, 230, 620, 100, "SI 4 pattes ET moustaches ?", fill=TEAL_L, stroke=TEAL, fs=34)
    s.arrow(620, 280, 380, 380); s.text(460, 310, "oui", fs=28, color=GREEN, weight="bold")
    s.arrow(980, 280, 1220, 380); s.text(1140, 310, "non", fs=28, color=RED, weight="bold")
    s.cbox(380, 440, 520, 100, "SI miaule ?", fill=TEAL_L, stroke=TEAL, fs=34)
    s.cbox(1220, 440, 420, 100, "ALORS pas un chat", fill=RED_L, stroke=RED, fs=34)
    s.arrow(260, 490, 180, 590); s.text(185, 530, "oui", fs=28, color=GREEN, weight="bold")
    s.arrow(500, 490, 580, 590); s.text(575, 530, "non", fs=28, color=RED, weight="bold")
    s.cbox(180, 650, 300, 100, "ALORS chat", fill=GREEN_L, stroke=GREEN, fs=34, weight="bold")
    s.cbox(600, 650, 380, 100, "ALORS pas un chat", fill=RED_L, stroke=RED, fs=34)
    s.text(1220, 650, "Règles écrites\npar des humains", fs=38, color=TEAL, weight="bold")
    s.save(out("systeme_expert.svg"))


def classic_vs_ml():
    s = SVG(1600, 720)
    for k, (title, a, b, res, col, colL) in enumerate([
            ("Programmation classique / système expert", "Règles", "Données", "Réponses", TEAL, TEAL_L),
            ("Apprentissage automatique (Machine Learning)", "Données", "Réponses", "Règles", ORANGE, ORANGE_L)]):
        y = 60 + k * 340
        s.text(800, y, title, fs=40, weight="bold", color=col)
        s.box(120, y + 50, 300, 90, a, fill=colL, fs=36)
        s.box(120, y + 160, 300, 90, b, fill=colL, fs=36)
        s.arrow(430, y + 95, 590, y + 150); s.arrow(430, y + 205, 590, y + 160)
        s.box(600, y + 90, 400, 120, "Ordinateur", fill=col, fs=40, color=WHITE, weight="bold")
        s.arrow(1010, y + 150, 1170, y + 150)
        s.box(1180, y + 90, 320, 120, res, fill=WHITE, stroke=col, sw=5, fs=40, weight="bold")
    s.save(out("classique_vs_ml.svg"))


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
    s.arrow(590, 320, 760, 320, sw=7)
    s.text(675, 280, "entraînement", fs=26, color=MUTED)
    s.cbox(950, 320, 340, 200, "Modèle\n(fonction apprise)", fill=ORANGE, color=WHITE, fs=36, weight="bold")
    s.arrow(1130, 320, 1260, 320, sw=7)
    s.rect(1280, 190, 260, 260, fill=WHITE, stroke=MUTED, sw=4, dash="12 10")
    s.text(1410, 290, "🐈", fs=110)
    s.text(1410, 400, "chat : 97 %", fs=32, color=GREEN, weight="bold")
    s.text(1410, 500, "nouvelle image", fs=28, color=MUTED, italic=True)
    s.save(out("chat_ml.svg"))


# ---------------------------------------------------------------- réseau de neurones
def tiny_network(name="reseau_mini.svg", weights=True):
    s = SVG(1600, 720)
    xs = [(250, 120 + i * 160) for i in range(4)]
    hs = [(800, 200), (800, 520)]
    o = (1330, 360)
    W = [[0.8, -0.3, None, None], [None, None, 1.2, 0.5]]
    for j, (hx, hy) in enumerate(hs):
        for i, (xx, xy) in enumerate(xs):
            w = W[j][i]
            if w is None:
                continue
            col = TEAL if w > 0 else RED
            s.line(xx + 50, xy, hx - 70, hy, color=col, sw=3 + 5 * abs(w))
            if weights:
                mx, my = (xx + hx) / 2, (xy + hy) / 2
                s.cbox(mx, my - 5, 90, 50, f"{w:+.1f}", fill=WHITE, stroke=col, fs=26, rx=25)
    for j, (hx, hy) in enumerate(hs):
        w = [0.9, -0.6][j]
        col = TEAL if w > 0 else RED
        s.line(hx + 70, hy, o[0] - 70, o[1], color=col, sw=3 + 5 * abs(w))
        if weights:
            s.cbox((hx + o[0]) / 2, (hy + o[1]) / 2, 90, 50, f"{w:+.1f}", fill=WHITE, stroke=col, fs=26, rx=25)
    for i, (xx, xy) in enumerate(xs):
        s.circle(xx, xy, 50, fill=LIGHT, stroke=INK)
        s.text(xx, xy, f"x{'₁₂₃₄'[i]}", fs=34)
    for hx, hy in hs:
        s.circle(hx, hy, 70, fill=ORANGE_L, stroke=ORANGE, sw=5)
        s.text(hx, hy, "neurone", fs=26)
    s.circle(o[0], o[1], 70, fill=TEAL, stroke=INK)
    s.text(o[0], o[1], "sortie", fs=28, color=WHITE, weight="bold")
    s.text(250, 700, "entrées", fs=28, color=MUTED, italic=True)
    if weights:
        s.text(1060, 690, "les poids = les « boutons » à régler", fs=30, color=TEAL, italic=True)
    s.save(out(name))


def scale_params():
    s = SVG(1600, 700)
    data = [("Notre petit\nréseau", 8, "8"), ("Reconnaître des\nchiffres (1998)", 6e4, "60 000"),
            ("GPT-2\n(2019)", 1.5e9, "1,5 milliard"), ("GPT-3\n(2020)", 1.75e11, "175 milliards"),
            ("Grands modèles\nactuels", 1e12, "~1 000 milliards ?")]
    base_y, top = 560, 90
    lmax = 12.5
    for i, (lab, v, txt) in enumerate(data):
        x = 130 + i * 290
        h = (base_y - top) * max(np.log10(v), 0.3) / lmax
        col = ORANGE if i == len(data) - 1 else TEAL
        s.rect(x, base_y - h, 190, h, fill=col, rx=10)
        s.text(x + 95, base_y - h - 35, txt, fs=30, weight="bold", color=col)
        s.text(x + 95, base_y + 60, lab, fs=26)
    s.line(90, base_y, 1560, base_y, color=INK, sw=3)
    s.text(90, 40, "nombre de « boutons » (paramètres), échelle logarithmique", fs=28, color=MUTED, anchor="start")
    s.save(out("echelle_parametres.svg"))


# ---------------------------------------------------------------- entraînement
def training_loop():
    s = SVG(1600, 780)
    cx, cy, R = 800, 400, 280
    steps = [("Exemple\n(donnée)", LIGHT, INK), ("Prédiction\ndu modèle", ORANGE_L, INK),
             ("Comparaison avec\nla bonne réponse", TEAL_L, INK), ("Erreur", RED_L, RED),
             ("On ajuste\nles boutons", GREEN_L, GREEN)]
    n = len(steps)
    pts = []
    for i in range(n):
        a = -np.pi / 2 + 2 * np.pi * i / n
        pts.append((cx + R * 1.55 * np.cos(a), cy + R * np.sin(a)))
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # courbure vers l'extérieur
        dx, dy = mx - cx, my - cy
        d = np.hypot(dx, dy)
        qx, qy = mx + dx / d * 70, my + dy / d * 70
        f = 0.28
        s.curve_arrow(x1 + (qx - x1) * f, y1 + (qy - y1) * f, qx, qy,
                      x2 + (qx - x2) * f, y2 + (qy - y2) * f, color=MUTED, sw=5)
    for (x, y), (lab, fill, col) in zip(pts, steps):
        s.cbox(x, y, 330, 120, lab, fill=fill, fs=30, color=col, weight="bold")
    s.text(cx, cy - 20, "× des millions", fs=44, weight="bold", color=TEAL)
    s.text(cx, cy + 35, "voire des milliards de fois", fs=30, color=MUTED)
    s.save(out("boucle_entrainement.svg"))


def pipeline():
    s = SVG(1600, 560)
    steps = [("Données", "collecter\ndes textes", LIGHT),
             ("Préparation", "nettoyer,\nfiltrer, découper", LIGHT),
             ("Pré-entraînement", "prédire la suite\nsur des milliards\nde phrases", ORANGE_L),
             ("Fine-tuning", "apprendre\nà répondre\n(dialogues)", TEAL_L),
             ("Alignement", "préférences\nhumaines :\nutile, honnête,\nprudent", PURPLE_L),
             ("Évaluation", "tests, mesures,\nrecherche\nde failles", GREEN_L),
             ("Déploiement", "mise à\ndisposition\ndu public", LIGHT)]
    w, gap = 200, 22
    x0 = (1600 - (7 * w + 6 * gap)) / 2
    for i, (t, d, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        s.box(x, 60, w, 120, t if len(t) < 12 else t.replace("-", "-\n"), fill=c, fs=29, weight="bold")
        s.text(x + w / 2, 320, d, fs=29, color=MUTED)
        if i < 6:
            s.arrow(x + w + 3, 120, x + w + gap - 3, 120, sw=4, head=14)
    s.text(800, 500, "chaque étape façonne le comportement final", fs=32, italic=True, color=TEAL)
    s.save(out("pipeline.svg"))


def data_model_behavior():
    s = SVG(1600, 400)
    labs = [("Données", LIGHT, INK), ("Modèle", ORANGE, WHITE), ("Comportement", TEAL, WHITE)]
    for i, (l, f, c) in enumerate(labs):
        s.cbox(300 + i * 500, 200, 360, 150, l, fill=f, color=c, fs=44, weight="bold")
        if i < 2:
            s.arrow(490 + i * 500, 200, 610 + i * 500, 200, sw=8, head=28)
    s.save(out("donnees_modele.svg"))


# ---------------------------------------------------------------- LLM
def tokens_split():
    s = SVG(1600, 640)
    phrase = "La bibliothèque ouvre à 9h."
    rows = [("Caractères", list(phrase), LIGHT, 42),
            ("Mots", ["La", "bibliothèque", "ouvre", "à", "9h", "."], TEAL_L, None),
            ("Tokens", ["La", " biblio", "thèque", " ouvre", " à", " 9", "h", "."], ORANGE_L, None)]
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
        s.text(1540, y + 45, str(n), fs=44, weight="bold", color=[MUTED, TEAL, ORANGE][r])
    s.text(1540, 20, "unités", fs=24, color=MUTED)
    notes = [("Caractères", "peu de symboles, mais des séquences très longues", MUTED),
             ("Mots", "séquences courtes, mais vocabulaire infini (noms, fautes, néologismes…)", TEAL),
             ("Tokens", "le compromis : des morceaux fréquents, ~50 000 à 200 000 au total", ORANGE)]
    for i, (a, b, c) in enumerate(notes):
        y = 510 + i * 44
        s.text(260, y, a + " :", fs=28, anchor="end", weight="bold", color=c)
        s.text(280, y, b, fs=28, anchor="start", color=INK)
    s.save(out("tokens.svg"))


def bars(name, title, items, highlight=None, question=False, colors=None):
    s = SVG(1600, 120 + 95 * len(items))
    s.text(800, 50, title, fs=44, weight="bold")
    mx = max(p for _, p in items)
    for i, (t, p) in enumerate(items):
        y = 120 + i * 95
        s.text(360, y + 35, t, fs=38, anchor="end")
        col = ORANGE if (highlight is not None and i in highlight) else TEAL
        s.rect(390, y, 950 * p / mx, 70, fill=col, rx=8)
        s.text(390 + 950 * p / mx + 20, y + 35, f"{p:.0f} %", fs=34, anchor="start", weight="bold", color=col)
    if question:
        s.text(1520, 120 + 95, "?", fs=150, color=ORANGE, weight="bold")
    s.save(out(name))


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
        s.text(x0 + 250, 110, lab, fs=32, weight="bold", color=[TEAL, INK, ORANGE][k])
        for i, t in enumerate(toks):
            y = 160 + i * 64
            s.text(x0 + 140, y + 22, t, fs=30, anchor="end")
            s.rect(x0 + 155, y, 300 * p[i] + 2, 48, fill=[TEAL, MUTED, ORANGE][k], rx=6)
            s.text(x0 + 165 + 300 * p[i], y + 22, f"{100 * p[i]:.0f}%", fs=26, anchor="start", color=MUTED)
    s.save(out("temperature.svg"))


def chat_as_text():
    s = SVG(1600, 700)
    s.text(380, 40, "Ce que l'on voit", fs=36, weight="bold", color=TEAL)
    s.box(80, 90, 520, 90, "Bonjour ! Un roman pour l'été ?", fill=TEAL_L, fs=28)
    s.box(200, 200, 520, 130, "Volontiers : aimez-vous plutôt\nles policiers ou les sagas ?", fill=LIGHT, fs=28)
    s.box(80, 350, 520, 90, "Plutôt les policiers.", fill=TEAL_L, fs=28)
    s.box(200, 460, 520, 90, "…", fill=LIGHT, fs=40)
    s.arrow(760, 330, 860, 330, sw=8, head=28)
    s.text(1210, 40, "Ce que le modèle reçoit", fs=36, weight="bold", color=ORANGE)
    s.rect(880, 80, 660, 520, fill=WHITE, stroke=ORANGE, sw=4)
    lines = [("Système : Tu es un assistant utile.", MUTED),
             ("Utilisateur : Bonjour ! Un roman pour l'été ?", INK),
             ("Assistant : Volontiers : aimez-vous plutôt", INK),
             ("   les policiers ou les sagas ?", INK),
             ("Utilisateur : Plutôt les policiers.", INK),
             ("Assistant :", ORANGE)]
    for i, (l, c) in enumerate(lines):
        s.text(910, 130 + i * 62, l, fs=26, anchor="start", color=c, weight="bold" if c == ORANGE else "normal")
    s.rect(1080, 430, 36, 44, fill=ORANGE, rx=4, opacity=0.6)
    s.text(1210, 550, "un seul long texte → prédire la suite", fs=28, italic=True, color=ORANGE)
    s.text(800, 660, "Pas de mémoire propre : tout l'historique est relu à chaque réponse.", fs=30, color=MUTED)
    s.save(out("conversation.svg"))


def human_like():
    s = SVG(1600, 740)
    cx, cy = 800, 380
    s.circle(cx, cy, 150, fill=ORANGE, stroke=None)
    s.text(cx, cy, "Impression\nd'intelligence", fs=36, color=WHITE, weight="bold")
    items = [("Langage fluide", "🗣️"), ("Contexte", "📚"), ("Continuité", "🔗"),
             ("Raisonnement\napparent", "🧩"), ("S'adapte à\nl'interlocuteur", "🤝")]
    for i, (t, e) in enumerate(items):
        a = -np.pi / 2 + 2 * np.pi * i / len(items)
        x, y = cx + 560 * np.cos(a), cy + 290 * np.sin(a)
        s.line(cx + 150 * np.cos(a), cy + 150 * np.sin(a), x - 130 * np.cos(a), y - 60 * np.sin(a), color=MUTED, sw=3, dash="8 8")
        s.cbox(x, y, 330, 130, "", fill=TEAL_L)
        s.text(x - 110, y, e, fs=50)
        s.text(x + 40, y, t, fs=30, weight="bold")
    s.save(out("humain.svg"))


def chain_of_thought():
    s = SVG(1600, 760)
    s.box(100, 20, 1400, 130, "3 étages × 12 rayonnages × 40 livres. 15 % sont prêtés.\nCombien de livres restent en rayon ?",
          fill=LIGHT, fs=34)
    # direct
    s.text(380, 210, "Réponse directe", fs=34, weight="bold", color=RED)
    s.arrow(380, 240, 380, 330)
    s.cbox(380, 400, 360, 120, "« 1 260 »  ✗", fill=RED_L, stroke=RED, fs=40, weight="bold")
    # étapes
    s.text(1120, 210, "Avec étapes intermédiaires", fs=34, weight="bold", color=GREEN)
    steps = ["3 × 12 = 36 rayonnages", "36 × 40 = 1 440 livres", "15 % de 1 440 = 216", "1 440 − 216 = 1 224"]
    for i, st in enumerate(steps):
        y = 250 + i * 95
        s.cbox(1120, y + 35, 520, 72, st, fill=GREEN_L if i < 3 else GREEN, fs=30,
               color=INK if i < 3 else WHITE, weight="bold" if i == 3 else "normal")
        if i < 3:
            s.arrow(1120, y + 72, 1120, y + 95, head=14, sw=4)
    s.text(800, 690, "Chaque étape écrite devient du contexte pour prédire la suivante.",
           fs=32, italic=True, color=TEAL)
    s.save(out("chain_of_thought.svg"))


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
        s.text(x0 + 360, 45, title, fs=40, weight="bold", color=[TEAL, ORANGE][k])
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
    s.text(420, 40, "1. Quels textes garder ?", fs=36, weight="bold", color=TEAL)
    corpora = [("Pages web", True), ("Livres", True), ("Wikipédia", True), ("Code informatique", True),
               ("Forums", False), ("Presse", True), ("Textes en d'autres langues", False)]
    for i, (c, keep) in enumerate(corpora):
        y = 80 + i * 82
        s.box(120, y, 480, 66, c, fill=GREEN_L if keep else RED_L, fs=28,
              color=INK if keep else MUTED)
        s.text(650, y + 33, "✓" if keep else "✗", fs=44, weight="bold", color=GREEN if keep else RED)
        if not keep:
            s.line(150, y + 33, 570, y + 33, color=RED, sw=4)
    s.text(1130, 40, "2. Quel poids donner à chacun ?", fs=36, weight="bold", color=ORANGE)
    mix = [("Pages web", 0.45, TEAL), ("Livres", 0.15, ORANGE), ("Wikipédia", 0.08, PURPLE),
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
    s.arrow(1130, 590, 1130, 620, sw=6)
    s.cbox(1130, 665, 320, 80, "Modèle", fill=TEAL, color=WHITE, fs=36, weight="bold")
    s.text(420, 680, "Des choix humains, avant tout calcul.", fs=30, italic=True, color=RED, weight="bold")
    s.save(out("biais_entrainement.svg"))


def usage_bias():
    s = SVG(1600, 700)
    s.rect(40, 40, 720, 420, fill=ORANGE_L, stroke=ORANGE, sw=4, dash="14 10")
    s.text(400, 85, "Instructions ajoutées (souvent invisibles)", fs=30, weight="bold", color=ORANGE)
    rules = ["« N'explique pas comment fabriquer une bombe. »",
             "« Ne fais la promotion d'aucun parti politique. »",
             "« Reste poli et nuancé. »"]
    for i, r in enumerate(rules):
        s.box(70, 130 + i * 105, 660, 85, r, fill=WHITE, fs=26)
    s.box(40, 510, 720, 110, "Question de l'utilisateur", fill=LIGHT, fs=32, weight="bold")
    s.arrow(770, 250, 930, 340, sw=5, color=ORANGE)
    s.arrow(770, 565, 930, 400, sw=5)
    s.cbox(1060, 370, 240, 180, "Modèle", fill=TEAL, color=WHITE, fs=40, weight="bold")
    s.arrow(1185, 370, 1300, 370, sw=5)
    s.cbox(1430, 370, 240, 150, "Réponse", fill=WHITE, stroke=MUTED, fs=34)
    s.text(1170, 580, "Des règles légitimes…\nmais qui restent des choix.", fs=30, italic=True, color=RED, weight="bold")
    s.save(out("biais_usage.svg"))


def agents_fanout(name, instructions, synth="Synthèse\nhumaine", title_left="Même\nproblème"):
    s = SVG(1600, 700)
    n = len(instructions)
    s.cbox(160, 350, 250, 160, title_left, fill=LIGHT, fs=34, weight="bold")
    for i, t in enumerate(instructions):
        y = 350 + (i - (n - 1) / 2) * 125
        s.arrow(290, 350, 450, y, sw=4)
        s.box(460, y - 50, 560, 100, t, fill=TEAL_L if i % 2 == 0 else ORANGE_L, fs=28)
        s.arrow(1030, y, 1230, 350, sw=4, color=MUTED)
    s.cbox(1380, 350, 280, 180, synth, fill=GREEN, color=WHITE, fs=34, weight="bold")
    s.save(out(name))


def research_before_after():
    s = SVG(1600, 760)
    s.text(270, 40, "Avant", fs=40, weight="bold", color=TEAL)
    steps = ["Hypothèse", "Recherche\nbibliographique", "Quelques pistes", "Expérimentation"]
    for i, t in enumerate(steps):
        y = 90 + i * 165
        s.cbox(270, y + 55, 380, 115, t, fill=TEAL_L, fs=30)
        if i < 3:
            s.arrow(270, y + 115, 270, y + 160)
    s.line(560, 40, 560, 720, color=LIGHT, sw=6)
    s.text(1080, 40, "Avec des agents", fs=40, weight="bold", color=ORANGE)
    s.cbox(720, 380, 200, 110, "Question", fill=LIGHT, fs=32, weight="bold")
    ags = ["Agent 1 : hypothèse A", "Agent 2 : hypothèse B", "Agent 3 : autre domaine",
           "Agent 4 : objections", "…  × 50"]
    for i, t in enumerate(ags):
        y = 120 + i * 130
        s.arrow(820, 380, 910, y + 40, sw=4)
        s.box(920, y, 400, 80, t, fill=ORANGE_L, fs=26)
        s.arrow(1330, y + 40, 1410, 380, sw=3)
    s.cbox(1490, 380, 170, 150, "Synthèse\nhumaine", fill=GREEN, color=WHITE, fs=28, weight="bold")
    s.save(out("recherche.svg"))


def shared_source():
    s = SVG(1600, 700)
    rng = np.random.default_rng(3)
    cx, cy = 800, 560
    s.cbox(cx, cy, 560, 140, "Même modèle · mêmes données\nmêmes angles morts", fill=RED_L, stroke=RED, fs=32, weight="bold")
    for i in range(50):
        a = np.pi * (0.06 + 0.88 * i / 49)
        r = 520 + rng.uniform(-40, 40)
        x, y = cx - r * np.cos(a) * 1.35, cy - 80 - r * np.sin(a) * 0.9
        s.line(x, y, cx + (x - cx) * 0.15, cy - 70, color=RED, sw=1.5, opacity=0.35)
        s.circle(x, y, 17, fill=ORANGE, stroke=None)
    s.text(800, 250, "50 agents", fs=54, weight="bold", color=ORANGE)
    s.text(800, 315, "≠ 50 avis indépendants", fs=40, color=INK)
    s.save(out("agents_biais_communs.svg"))


# ---------------------------------------------------------------- humain
def better_vs_preferred():
    s = SVG(1600, 680)
    rows = [("Musée", "📱", "Tablette", "plus d'informations", "🧑‍🏫", "Visite guidée", "on préfère souvent"),
            ("Musique", "🎧", "MP3", "plus pratique, parfait", "🎤", "Concert", "on y va quand même")]
    s.text(560, 40, "« objectivement meilleur »", fs=34, color=TEAL, weight="bold")
    s.text(1200, 40, "« socialement préféré »", fs=34, color=ORANGE, weight="bold")
    for i, (dom, e1, t1, d1, e2, t2, d2) in enumerate(rows):
        y = 100 + i * 280
        s.text(130, y + 110, dom, fs=40, weight="bold")
        s.box(300, y, 520, 220, "", fill=TEAL_L)
        s.text(400, y + 110, e1, fs=100)
        s.text(640, y + 85, t1, fs=38, weight="bold")
        s.text(640, y + 145, d1, fs=26, color=MUTED)
        s.text(880, y + 110, "≠", fs=80, color=INK, weight="bold")
        s.box(940, y, 520, 220, "", fill=ORANGE_L)
        s.text(1040, y + 110, e2, fs=100)
        s.text(1280, y + 85, t2, fs=38, weight="bold")
        s.text(1280, y + 145, d2, fs=26, color=MUTED)
    s.save(out("meilleur_vs_prefere.svg"))


def teacher():
    s = SVG(1600, 760)
    for k, (t, steps, col, colL) in enumerate([
            ("AVANT", ["Produire l'explication", "Faire l'exercice", "Corriger"], TEAL, TEAL_L),
            ("APRÈS", ["Choisir l'explication", "Accompagner", "Motiver", "Repérer les difficultés", "Interagir"], ORANGE, ORANGE_L)]):
        x = 420 + k * 760
        s.text(x, 45, t, fs=44, weight="bold", color=col)
        n = len(steps)
        for i, st in enumerate(steps):
            y = 100 + i * (620 / n)
            s.cbox(x, y + 45, 480, 88, st, fill=colL, fs=32)
            if i < n - 1:
                s.arrow(x, y + 92, x, y + 620 / n - 2, head=14, sw=4)
    s.arrow(700, 380, 900, 380, sw=8, head=28, color=MUTED)
    s.text(800, 330, "l'IA", fs=30, color=MUTED, italic=True)
    s.save(out("professeur.svg"))


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


def cost_bars():
    s = SVG(1600, 720)
    tasks = [("Créer un faux site crédible", 40, 1.5), ("Rédiger 100 mails sans fautes", 30, 0.5),
             ("Traduire", 10, 0.1), ("Personnaliser chaque message", 50, 0.3), ("Générer des variantes", 20, 0.1)]
    cols = [TEAL, ORANGE, PURPLE, GREEN, RED]
    tot = sum(t[1] for t in tasks)
    scale = 1150 / tot
    for k, (lab, idx) in enumerate([("Avant", 1), ("Avec l'IA", 2)]):
        y = 150 + k * 250
        s.text(260, y + 60, lab, fs=42, weight="bold", anchor="end")
        x = 300
        for (t, *v), c in zip(tasks, cols):
            w = v[idx - 1] * scale
            s.rect(x, y, max(w, 4), 120, fill=c, rx=4)
            x += w
        if k == 1:
            s.text(x + 30, y + 60, "← le coût marginal s'effondre", fs=34, anchor="start", color=RED, weight="bold")
    for i, (t, *_), in enumerate(tasks):
        x = 120 + (i % 3) * 490
        y = 600 + (i // 3) * 60
        s.rect(x, y - 18, 36, 36, fill=cols[i], rx=6)
        s.text(x + 50, y, t, fs=26, anchor="start")
    s.text(800, 60, "Effort humain nécessaire (ordres de grandeur illustratifs)", fs=32, color=MUTED, italic=True)
    s.save(out("cout_manipulation.svg"))


def chatbot_vs_agent():
    s = SVG(1600, 760)
    s.text(330, 40, "Chatbot", fs=42, weight="bold", color=TEAL)
    s.cbox(330, 150, 300, 100, "Utilisateur", fill=LIGHT, fs=32)
    s.arrow(330, 205, 330, 285)
    s.cbox(330, 350, 260, 110, "LLM", fill=TEAL, color=WHITE, fs=40, weight="bold")
    s.arrow(330, 410, 330, 490)
    s.cbox(330, 560, 300, 110, "📝 Texte", fill=TEAL_L, fs=34)
    s.text(330, 690, "reste dans le monde du texte", fs=28, color=MUTED, italic=True)
    s.line(680, 40, 680, 720, color=LIGHT, sw=6)
    s.text(1140, 40, "Agent qui peut agir", fs=42, weight="bold", color=ORANGE)
    s.cbox(1140, 150, 300, 100, "Utilisateur", fill=LIGHT, fs=32)
    s.arrow(1140, 205, 1140, 285)
    s.cbox(1140, 350, 260, 110, "LLM", fill=ORANGE, color=WHITE, fs=40, weight="bold")
    tools = [("🌐", "Web"), ("📁", "Fichiers"), ("⌨️", "Terminal"), ("✉️", "E-mail")]
    for i, (e, t) in enumerate(tools):
        x = 810 + i * 220
        s.arrow(1140, 410, x, 500, sw=4)
        s.cbox(x, 570, 190, 130, "", fill=ORANGE_L)
        s.text(x, 545, e, fs=50)
        s.text(x, 605, t, fs=28, weight="bold")
    s.text(1140, 700, "chaque sortie peut déclencher une action", fs=28, color=RED, italic=True, weight="bold")
    s.save(out("chatbot_vs_agent.svg"))


def hf_incident():
    s = SVG(1600, 720)
    steps = [("Évaluation interne\nd'OpenAI", "tester des capacités\nen cybersécurité", LIGHT, INK),
             ("L'agent sort\nde son bac à sable", "via une faille inconnue\n(« zero-day »)", ORANGE_L, INK),
             ("Entre chez\nHugging Face", "fichier de données piégé\n→ exécution de code", RED_L, INK),
             ("Vole des\nidentifiants", "se déplace entre\nles serveurs internes", RED_L, INK),
             ("Détecté", "par des outils de\ndétection d'anomalies", GREEN_L, INK)]
    w, gap = 270, 42
    x0 = (1600 - (5 * w + 4 * gap)) / 2
    s.line(x0, 90, x0 + 5 * w + 4 * gap, 90, color=MUTED, sw=4)
    s.text(x0, 45, "9 juillet 2026", fs=26, anchor="start", color=MUTED)
    s.text(x0 + 5 * w + 4 * gap, 45, "13 juillet 2026", fs=26, anchor="end", color=MUTED)
    for i, (t, d, c, col) in enumerate(steps):
        x = x0 + i * (w + gap)
        s.circle(x + w / 2, 90, 14, fill=ORANGE if 0 < i < 4 else TEAL)
        s.box(x, 140, w, 140, t, fill=c, fs=28, weight="bold")
        s.text(x + w / 2, 350, d, fs=26, color=MUTED)
        if i < 4:
            s.arrow(x + w + 4, 210, x + w + gap - 4, 210, sw=4, head=14)
    s.rect(160, 450, 1280, 170, fill=WHITE, stroke=ORANGE, sw=4)
    s.text(800, 500, "Objectif de l'agent, selon Hugging Face : « tricher » à l'évaluation", fs=32, weight="bold")
    s.text(800, 565, "aller chercher les solutions du test plutôt que résoudre l'exercice lui-même", fs=28, color=MUTED)
    s.text(800, 680, "≈ 17 600 actions automatisées reconstituées par Hugging Face, en ~4 jours", fs=28, color=RED, weight="bold")
    s.save(out("incident_hf.svg"))


def personalization():
    s = SVG(1600, 700)
    s.text(800, 45, "« Donne-moi les arguments sur X »", fs=38, italic=True, weight="bold")
    for k, (who, e, col, colL) in enumerate([("Personne A", "🧑", TEAL, TEAL_L), ("Personne B", "👩", ORANGE, ORANGE_L)]):
        y = 150 + k * 290
        s.text(110, y + 90, e, fs=100)
        s.text(110, y + 190, who, fs=28, weight="bold", color=col)
        s.arrow(210, y + 100, 470, 340 + (k * 2 - 1) * 60, sw=4, color=col)
        s.box(1130, y + 20, 400, 170, f"Réponse {'AB'[k]}", fill=colL, fs=38, weight="bold")
        s.arrow(890, 340 + (k * 2 - 1) * 60, 1120, y + 105, sw=4, color=col)
    s.cbox(680, 360, 420, 300, "", fill=LIGHT)
    for i, t in enumerate(["contexte", "historique", "formulation", "sources", "préférences implicites"]):
        s.text(680, 240 + i * 58, t, fs=30, color=INK if i < 4 else PURPLE)
    s.save(out("personnalisation.svg"))


def same_event():
    s = SVG(1600, 700)
    s.cbox(800, 80, 440, 110, "Même événement", fill=INK, color=WHITE, fs=38, weight="bold")
    for k, (p, col, colL) in enumerate([("Personne A", TEAL, TEAL_L), ("Personne B", ORANGE, ORANGE_L)]):
        x = 420 + k * 760
        s.arrow(800, 140, x, 250, sw=5)
        s.cbox(x, 300, 360, 100, p, fill=colL, fs=34, weight="bold")
        s.arrow(x, 355, x, 440, sw=5, color=col)
        s.cbox(x, 520, 420, 150, f"Contenu {'AB'[k]}", fill=col, color=WHITE, fs=40, weight="bold")
    s.text(800, 520, "≠", fs=110, weight="bold", color=MUTED)
    s.save(out("meme_evenement.svg"))


def jakesch():
    s = SVG(1600, 720)
    s.cbox(190, 340, 300, 180, "1 506\nparticipants", fill=LIGHT, fs=36, weight="bold")
    s.text(800, 45, "Écrire un texte : « les réseaux sociaux sont-ils bons pour la société ? »", fs=30, italic=True)
    groups = [("Écrit seul", "(groupe témoin)", LIGHT, INK),
              ("Avec une IA réglée\nsur « plutôt POUR »", "", TEAL_L, INK),
              ("Avec une IA réglée\nsur « plutôt CONTRE »", "", ORANGE_L, INK)]
    for i, (t, sub, c, col) in enumerate(groups):
        y = 150 + i * 190
        s.arrow(345, 340, 520, y + 70, sw=4)
        s.box(530, y, 460, 140, t + ("\n" + sub if sub else ""), fill=c, fs=28, weight="bold" if i else "normal")
        s.arrow(1000, y + 70, 1090, y + 70, sw=4)
    s.box(1100, 150, 440, 140, "Référence", fill=LIGHT, fs=30)
    s.box(1100, 340, 440, 140, "Textes plus « pour »\n+ opinion déplacée", fill=TEAL, color=WHITE, fs=28, weight="bold")
    s.box(1100, 530, 440, 140, "Textes plus « contre »\n+ opinion déplacée", fill=ORANGE, color=WHITE, fs=28, weight="bold")
    s.save(out("jakesch.svg"))


def takeaways_icon():
    pass


if __name__ == "__main__":
    roadmap()
    for i in range(5):
        roadmap(i, f"roadmap_{i + 1}.svg")
    info_balance()
    expert_system()
    classic_vs_ml()
    cats_ml()
    tiny_network()
    scale_params()
    training_loop()
    pipeline()
    data_model_behavior()
    tokens_split()
    bars("proba_chat.svg", "« Le chat est sur le … »",
         [("sol", 42), ("canapé", 38), ("lit", 15), ("toit", 3), ("…", 2)])
    bars("proba_egalite.svg", "« Pour le petit-déjeuner, je prends un … »",
         [("café", 34), ("thé", 33), ("croissant", 18), ("jus", 9), ("…", 6)],
         highlight={0, 1}, question=True)
    temperature_static()
    chat_as_text()
    human_like()
    chain_of_thought()
    two_biases()
    training_bias()
    usage_bias()
    agents_fanout("agents_consignes.svg",
                  ["« Essaie de démontrer A »", "« Démontre le contraire »",
                   "« Approche statistique »", "« Approche d'un autre domaine »",
                   "« Cherche les objections »"],
                  synth="Plus de\nperspectives")
    research_before_after()
    shared_source()
    better_vs_preferred()
    teacher()
    fake_media()
    cost_bars()
    chatbot_vs_agent()
    hf_incident()
    personalization()
    same_event()
    jakesch()
    print("figures générées dans", OUT)
