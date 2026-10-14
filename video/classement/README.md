# Film « Décision rendue, décision non reçue » (2 min 22)

Source : script de production v2 du 14 octobre 2026. Chaque date et chaque extrait renvoie à une pièce publiée (voir la page du film dans `/batonnier-hounkpatin/decision-rendue-decision-non-recue/`).

Reconstruction (modèles Kokoro dans `<modèles>`) :

```
python3 build.py <modèles> <sortie>        # voix, bande son, sous-titres, motion.html
NODE_PATH=<playwright> node render.js <sortie>/audio.wav classement-16-9.mp4
```

`build.py` met en cache les phrases de voix (dossier `<sortie>/cache`). Les extraits de pièces sont dans `img/` (recadrages des pages publiées ; les annotations rouges des originaux y sont effacées, sauf sur l'avis de classement, reproduit tel que le plaignant l'a numérisé).
