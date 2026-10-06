---
name: video-motion-design
description: Produire ou modifier une vidéo de motion design avec voix-off pour le site wadagni2026-verite.com (script par scènes, animation HTML rendue en MP4 avec ffmpeg, sous-titres, voix de synthèse Kokoro, intégration sur index.html). À utiliser pour toute nouvelle vidéo, toute retouche de texte ou de scène, ou toute régénération de la voix-off.
---

# Vidéo de motion design + voix-off (site wadagni2026-verite.com)

Chaîne éprouvée sur la vidéo « Le certificat contre les pièces officielles ». Tout est reproductible dans l'environnement cloud, sans logiciel de montage.

## Ligne éditoriale (consignes de l'éditeur, Gilles Féliho)
- **Chaque affirmation à l'écran renvoie à une pièce** (nom, date, numéro) : certificat d'acquit de droit du 20/10/2016, déclaration de décès CNHU-HKM, jugement n° 114/14 du 31/10/2014, lettre de Me Balley du 07/09/2023, lettre AIB du 05/10/2011, communiqué du 03/04/2013 (journal La Nation), etc. Lire la pièce avant de l'écrire ; ne jamais citer un chiffre de mémoire.
- **Affirmer ce que les pièces établissent**, sans « il conteste » : l'éditeur tient à un ton ferme. Les qualifications qu'il assume lui-même (« frauduleux », « impuni », « arnaque ») viennent de lui ; ne pas en ajouter d'autres, ne pas inventer de fait.
- Ne pas comparer des périmètres différents sans le dire (ex. 7 immeubles du certificat contre 39 immeubles France et Bénin du jugement). Pas de pourcentage non sourcé.
- **Le nom de Me BALLEY doit apparaître** : c'est l'élément central. Ne pas répéter un mot (ex. « successeur ») que l'éditeur a demandé de ne citer qu'une fois.
- **Ne pas retirer une scène ou une phrase dictée par l'éditeur** sans qu'il le demande. Quand un choix éditorial est ambigu, dire comment on l'a lu.
- La décision DCC 25-152 n'est plus dans la vidéo (Cour déclarée incompétente) ; ne la réintroduire que sur demande. Si on la cite, jamais comme « confirmant la fraude ».
- Éviter les liens non documentés. Ce qui n'a pas de pièce va dans la liste « à confirmer » donnée à l'éditeur, pas à l'écran.

## Fichiers
- `video/motion.html` : source de l'animation (scènes `<div class="scene" data-s data-e>` ; éléments `.el` avec `data-in` = délai relatif ; fonction `seek(t)` ; tableau `CUES` = sous-titres/voix-off `[début, fin, texte]` ; `DUR`).
- `video/render.js` : rend `motion.html` image par image (Playwright + Chromium, 24 i/s) et encode `motion-design.mp4` (ffmpeg, piste muette) + `motion-design.fr.vtt`.
- `video/voix/build_voix.py` : génère la voix (Kokoro `ff_siwis`, vitesse 1,1), découpe les phrases > 165 caractères, recale les scènes sur la voix, écrit `voix-off.wav`, `timeline.json` et `motion-voix.html`.
- `video/voix/render-voix.js` : rend `motion-voix.html` et mixe la voix → `motion-design-voix.mp4` + `.vtt`.
- `index.html` : section `#video` (lecteur `<video controls preload="none">`, poster, piste sous-titres non défaut, transcription dans `<details>`, balises `og:video`). Le lecteur lit `video/voix/motion-design-voix.mp4`.

## Procédure
1. **Script** : écrire les scènes (durée cible 90–120 s ; la voix à vitesse naturelle dure environ 1,35 × le texte affiché ; 3 minutes est acceptable si l'éditeur l'a validé). Une idée par scène, texte court à l'écran, mots-clés en couleur (rouge = faux/problème, vert = pièce, or = repère).
2. **Modifier `motion.html`** : scènes, `data-in`, `CUES`, `DUR`. Les cartes sont positionnées en absolu : vérifier qu'elles ne se chevauchent pas entre elles ni avec le sous-titre (bas de l'écran, 3 lignes ≈ 130 px).
3. **Contrôle visuel avant le rendu complet** : `ONLY=10,40,82 node render.js` produit `still-*.png` (à supprimer ensuite, ne pas les commiter), puis les regarder (`ffmpeg … hstack`).
4. **Rendu complet** (3–8 min) : toujours en arrière-plan (`nohup … &`) puis `Monitor`/`until grep DONE`. Ne jamais commiter avant la fin : le MP4 et les sous-titres sont produits par le script.
   `NODE_PATH=$(dirname $(readlink -f $(npm root -g)/playwright)) node render.js`
5. **Mettre à jour la transcription** de `index.html` (`<details class="video-transcript">`) à partir de `CUES`, et le titre de la section si la durée change.
6. **Voix** : voir ci-dessous. Puis régénérer `video/voix/*` et vérifier le chemin du lecteur dans `index.html`.
7. Commit, push, PR (seulement si l'éditeur la demande).

## Voix-off (Kokoro)
- Installer : `pip install kokoro-onnx soundfile`.
- Modèles (seul GitHub *releases* et PyPI sont joignables ; Hugging Face est bloqué) :
  `https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx` (92 Mo) → `kokoro.onnx` ; `…/voices-v1.0.bin` (28 Mo) → `voices.bin`.
- `python3 video/voix/build_voix.py <dossier_modèles> <dossier_sortie>` puis `node video/voix/render-voix.js <sortie>/voix.wav motion-design-voix.mp4`.
- **On ne peut pas écouter l'audio** : vérifier seulement durée, piste audio présente, niveau (`volumedetect`). Prévenir l'éditeur que la prononciation des noms (Féliho, Balley, Crinot, Adjagba Ischola) et des montants doit être écoutée par lui.
- Les mots mal prononcés se corrigent dans le texte de `CUES` (graphie phonétique pour la voix) sans toucher aux sous-titres affichés si besoin.
- Alternative : voix humaine enregistrée par l'éditeur ; `build_voix.py` donne les durées par segment pour recaler les scènes.

## Pièges rencontrés
- **`pkill -f motif`** tue aussi le shell qui contient le motif dans sa commande (exit 144) : tuer par PID (`pgrep -f` puis `kill <pid>`).
- Le **hook d'arrêt** signale « uncommitted changes » tant qu'un rendu tourne : attendre la fin du script (il commite et pousse), ne pas commiter une vidéo incomplète.
- Après fusion d'une PR, la **branche distante est supprimée** : `git push -u origin <branche>` (sans force) la recrée. Avant tout `--force-with-lease`, vérifier avec `git log origin/main..origin/<branche>` qu'il ne reste aucun commit non fusionné (un commit v13 a failli être écrasé).
- Si la PR a été fusionnée **avant** le dernier push, repartir de la branche distante (cherry-pick) plutôt que de `origin/main`.
- Le Chromium de test n'a pas H.264/AAC : impossible de tester la lecture réelle dans la page ; vérifier avec `ffprobe` (codecs `h264` + `aac`).
- **Écrire ≠ brancher** : après avoir produit un média, vérifier que `index.html` pointe bien dessus (la voix-off est restée un jour sans effet parce que le lecteur lisait encore l'ancien MP4).
- Les PDF fournis sont souvent des **scans** : `pdftotext` ne donne rien, il faut `pdftoppm -r 90..130` puis lire les images (pas d'OCR installé). Zoomer (`ffmpeg crop`) pour les cachets et dates manuscrites.
- `Lettre ouverte.pdf` : l'écrasement du fichier par un PDF corrigé a été refusé par le classeur de permissions ; ne pas insister, laisser l'éditeur trancher.

## Fait à ne pas refaire
- La page d'accueil a été alignée sur la vidéo (transcription, mention du jugement du 31/10/2014 à la place de « 1000 % », La Nation pour le communiqué). La lettre ouverte (PDF) contient encore l'ancienne formulation sur la Cour constitutionnelle : version corrigée à poser dans le dépôt sur autorisation.

## Plusieurs vidéos : un dossier par vidéo (convention actuelle)
- `video/<nom>/` contient `motion.html`, `build_voix.py`, `render-voix.js`, `motion-voix.html` (généré), `<nom>-voix.mp4`, `<nom>-voix.fr.vtt`, `poster.jpg`. Exemples : `video/jugement/` (page du jugement 114/14), `video/balley/` (page d'analyse « absence de lien »). Pour une nouvelle vidéo : copier `build_voix.py` et `render-voix.js` d'un dossier existant, remplacer le nom des fichiers de sortie, écrire `motion.html`.
- **Format des CUES** : `[début, fin, "sous-titre affiché", "texte lu (facultatif)"]`. Écrire **« Maître »** (jamais « Me ») dans le texte lu : `build_voix.py` refuse « Me » dans le texte lu. Dans le sous-titre, « Me » reste affiché.
- **Sous-titres ≤ 170 caractères par cue** (3 lignes maximum) : au-delà, le sous-titre à 4 lignes remonte sur les cartes et l'image. Découper en plusieurs cues ; les débuts de cues doivent tomber dans la fenêtre `data-s`/`data-e` de leur scène (c'est ce qui rattache cue et scène).
- **Images de pièces** dans une vidéo : chemin relatif depuis `video/<nom>/` (ex. `../../communique-succession-feliho-2013.png`). Recadrer l'image sur la zone utile (conteneur `overflow:hidden` + `<img>` positionnée) et surligner par des cadres `.el` ; un scan basse résolution reste peu lisible, donc doubler par une carte de texte avec la citation.
- **Intégration dans une page d'analyse** : `<section class="video-block container" id="video">` juste après le `</header>` (ou avant `<main>`), CSS `.video-block` dans le `<style>` de la page, lecteur `<video controls preload="none" playsinline poster=…>`, `<track kind="subtitles">` non défaut, lien de téléchargement, `<details>` avec la transcription (sous-titres regroupés par scène), balises `og:video` / `og:video:type`.
- **Rendu d'images de contrôle sans voix** : depuis `video/<nom>/`, `ONLY=7,30,62 NODE_PATH=… node ../render.js` (écrit `still-*.png` et `motion-design.fr.vtt` dans le dossier : les supprimer).
- Me Crinot est décédé : ne pas proposer « entendre Me Crinot » ; la page d'analyse le recommande encore, ne pas le reprendre dans les vidéos.
