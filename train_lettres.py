#!/usr/bin/env python3
"""Entraîne le petit réseau « 3 lettres → lettre suivante » utilisé par demos/lettres.html.

Corpus : Jules Verne, « Le tour du monde en quatre-vingts jours » (Project Gutenberg, domaine public),
téléchargé dans data/ au premier lancement.
Réseau : 3 × 27 entrées (un neurone par caractère possible à chaque position : espace + a…z),
une couche cachée sigmoïde, 27 sorties (softmax).
Résultat : demos/lettres_model.js (poids du réseau, chargés directement par la démo).

Usage : python3 train_lettres.py   (quelques dizaines de secondes)
"""

import json
import os
import re
import unicodedata
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_URL = "https://www.gutenberg.org/cache/epub/800/pg800.txt"
CORPUS = os.path.join(HERE, "data", "verne_tour_du_monde.txt")
OUT = os.path.join(HERE, "demos", "lettres_model.js")

ALPHABET = " abcdefghijklmnopqrstuvwxyz"
CTX, HIDDEN = 3, 20
EPOCHS, BATCH, LR = 25, 512, 0.01


def load_text():
    if not os.path.exists(CORPUS):
        os.makedirs(os.path.dirname(CORPUS), exist_ok=True)
        urllib.request.urlretrieve(CORPUS_URL, CORPUS)
    raw = open(CORPUS, encoding="utf-8").read()
    # retirer l'en-tête et la licence du Project Gutenberg
    start, end = raw.find("*** START"), raw.find("*** END")
    raw = raw[raw.find("\n", start) + 1:end]
    # minuscules, sans accents, uniquement espace + a…z
    txt = raw.lower().replace("œ", "oe").replace("æ", "ae")
    txt = "".join(c for c in unicodedata.normalize("NFD", txt) if not unicodedata.combining(c))
    txt = re.sub(f"[^{ALPHABET[1:]}]+", " ", txt)
    return txt.strip()


def main():
    rng = np.random.default_rng(0)
    txt = load_text()
    ids = np.array([ALPHABET.index(c) for c in txt])
    X = np.stack([ids[i:len(ids) - CTX + i] for i in range(CTX)], axis=1)   # (N, 3) indices
    Y = ids[CTX:]
    n, V = len(Y), len(ALPHABET)
    print(f"{n} exemples")

    # paramètres : W1 (3·27 × H), b1, W2 (H × 27), b2
    W1 = rng.normal(0, 0.5, (CTX * V, HIDDEN)); b1 = np.zeros(HIDDEN)
    W2 = rng.normal(0, 0.5, (HIDDEN, V)); b2 = np.zeros(V)
    params = [W1, b1, W2, b2]
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

    model = {"alphabet": ALPHABET, "ctx": CTX, "hidden": HIDDEN,
             "source": "Jules Verne, Le tour du monde en quatre-vingts jours (Project Gutenberg)",
             "accuracy": round(float(acc), 3),
             "W1": np.round(W1, 3).tolist(), "b1": np.round(b1, 3).tolist(),
             "W2": np.round(W2, 3).tolist(), "b2": np.round(b2, 3).tolist()}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// Généré par train_lettres.py : ne pas modifier à la main.\n")
        f.write("const MODEL = " + json.dumps(model, separators=(",", ":")) + ";\n")
    print("→", OUT)


if __name__ == "__main__":
    main()
