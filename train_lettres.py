#!/usr/bin/env python3
"""Entraîne le petit réseau « 3 lettres → lettre suivante » utilisé par demos/lettres.html.

Corpus (Project Gutenberg, domaine public, téléchargés dans data/ au premier lancement) :
  - français : Jules Verne, « Le tour du monde en quatre-vingts jours »
  - anglais  : sa traduction « Around the World in Eighty Days »
On exporte aussi un réseau aléatoire (non entraîné), pour comparaison.
Réseau : 3 × 27 entrées (un neurone par caractère possible à chaque position : espace + a…z),
une couche cachée sigmoïde, 27 sorties (softmax).
Résultat : demos/lettres_model.js (poids des 3 réseaux, chargés directement par la démo).

Usage : python3 train_lettres.py   (quelques dizaines de secondes)
"""

import json
import os
import re
import unicodedata
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CORPORA = {
    "fr": ("https://www.gutenberg.org/cache/epub/800/pg800.txt", "verne_tour_du_monde.txt",
           "Français (entraîné sur Jules Verne)"),
    "en": ("https://www.gutenberg.org/cache/epub/103/pg103.txt", "verne_around_the_world.txt",
           "Anglais (entraîné sur Jules Verne)"),
}
OUT = os.path.join(HERE, "demos", "lettres_model.js")

ALPHABET = " abcdefghijklmnopqrstuvwxyz"
CTX, HIDDEN = 3, 20
EPOCHS, BATCH, LR = 25, 512, 0.01


def load_text(lang):
    url, name, _ = CORPORA[lang]
    path = os.path.join(HERE, "data", name)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)
    raw = open(path, encoding="utf-8").read()
    # retirer l'en-tête et la licence du Project Gutenberg
    start, end = raw.find("*** START"), raw.find("*** END")
    raw = raw[raw.find("\n", start) + 1:end]
    # minuscules, sans accents, uniquement espace + a…z
    txt = raw.lower().replace("œ", "oe").replace("æ", "ae")
    txt = "".join(c for c in unicodedata.normalize("NFD", txt) if not unicodedata.combining(c))
    txt = re.sub(f"[^{ALPHABET[1:]}]+", " ", txt)
    return txt.strip()


def init_params(rng):
    V = len(ALPHABET)
    return [rng.normal(0, 0.5, (CTX * V, HIDDEN)), np.zeros(HIDDEN),
            rng.normal(0, 0.5, (HIDDEN, V)), np.zeros(V)]


def export(params, label, acc=None):
    W1, b1, W2, b2 = params
    return {"label": label, "accuracy": None if acc is None else round(float(acc), 3),
            "W1": np.round(W1, 3).tolist(), "b1": np.round(b1, 3).tolist(),
            "W2": np.round(W2, 3).tolist(), "b2": np.round(b2, 3).tolist()}


def train(lang):
    rng = np.random.default_rng(0)
    txt = load_text(lang)
    ids = np.array([ALPHABET.index(c) for c in txt])
    X = np.stack([ids[i:len(ids) - CTX + i] for i in range(CTX)], axis=1)   # (N, 3) indices
    Y = ids[CTX:]
    n, V = len(Y), len(ALPHABET)
    print(f"[{lang}] {n} exemples")

    # paramètres : W1 (3·27 × H), b1, W2 (H × 27), b2
    params = init_params(rng)
    W1, b1, W2, b2 = params
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    offs = np.arange(CTX) * V
    t = 0

    def forward(xb):
        h = 1 / (1 + np.exp(-(W1[xb + offs].sum(axis=1) + b1)))   # entrée « one-hot » = somme de 3 lignes
        z = h @ W2 + b2
        z -= z.max(axis=1, keepdims=True)
        p = np.exp(z); p /= p.sum(axis=1, keepdims=True)
        return h, p

    for ep in range(EPOCHS):
        perm = rng.permutation(n)
        for k in range(0, n, BATCH):
            idx = perm[k:k + BATCH]
            xb, yb = X[idx], Y[idx]
            h, p = forward(xb)
            dz = p; dz[np.arange(len(yb)), yb] -= 1; dz /= len(yb)          # softmax + entropie croisée
            gW2, gb2 = h.T @ dz, dz.sum(0)
            dh = (dz @ W2.T) * h * (1 - h)
            gW1 = np.zeros_like(W1)
            for c in range(CTX):
                np.add.at(gW1, xb[:, c] + offs[c], dh)
            grads = [gW1, dh.sum(0), gW2, gb2]
            t += 1
            for i, (pr, g) in enumerate(zip(params, grads)):             # Adam
                m[i] = 0.9 * m[i] + 0.1 * g; v[i] = 0.999 * v[i] + 0.001 * g * g
                pr -= LR * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-8)
        _, p = forward(X[:50000])
        acc = (p.argmax(1) == Y[:50000]).mean()
        loss = -np.log(p[np.arange(50000), Y[:50000]] + 1e-12).mean()
        print(f"époque {ep + 1} : erreur {loss:.3f}, bonne lettre en 1er choix {100 * acc:.1f} %")

    return export(params, CORPORA[lang][2], acc)


def main():
    models = {lang: train(lang) for lang in CORPORA}
    models["random"] = export(init_params(np.random.default_rng(1)), "Aléatoire (non entraîné)")
    data = {"alphabet": ALPHABET, "ctx": CTX, "hidden": HIDDEN, "models": models}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// Généré par train_lettres.py : ne pas modifier à la main.\n")
        f.write("const MODELS = " + json.dumps(data, separators=(",", ":")) + ";\n")
    print("→", OUT)


if __name__ == "__main__":
    main()
