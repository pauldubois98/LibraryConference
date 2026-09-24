# IA & société

Slides: <https://pauldubois98.github.io/LibraryConference/slides.html><br>
_`S` notes orateur, `F` plein écran, `Échap` vue d'ensemble._

Conférence de découverte du fonctionnement de l'IA, en vulgarisation, et introduction aux impacts sociétaux de l'IA : fake news, biais, éthique, bulles d'information, démocratie et IA.

- **Lieu** : Médiathèque Départementale de la Haute-Garonne
- **Date** : Mardi 29 septembre 2026, 9 h
- **Langue** : Français

### Demos:

- [Réseau](https://pauldubois98.github.io/LibraryConference/demos/reseau.html)
- [Entrainement](https://pauldubois98.github.io/LibraryConference/demos/entrainement.html)
- [Lettres](https://pauldubois98.github.io/LibraryConference/demos/lettres.html)
- [Token](https://pauldubois98.github.io/LibraryConference/demos/token.html)
- [Température](https://pauldubois98.github.io/LibraryConference/demos/temperature.html)


-----

### Construire les slides

```sh
python3 build.py          # génère figures/*.svg puis slides.html (pandoc + reveal.js)
python3 train_lettres.py  # (optionnel) réentraîne le réseau de la démo « lettre suivante »
```
