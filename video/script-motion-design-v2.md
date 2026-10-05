# Motion design — script v2 (90–120 s)

Principes : chaque affirmation à l'écran renvoie à une pièce numérotée ; la DCC 25-152 est présentée telle qu'elle est (incompétence, faits non écartés) ; sous-titres FR obligatoires (version EN pour la diaspora) ; voix posée ≈ 140–150 mots/min.

## Scène 1 — Accroche (0:00–0:12)
Visuel : fond sombre ; la pièce réelle (certificat du 20/10/2016, données de tiers floutées) apparaît, un passage se surligne. Pas de déformation de l'image.
Voix-off : « Un certificat d'acquit de droit. Un notaire présenté comme mandataire. Un héritier qui affirme ne lui avoir donné aucun mandat. »
Écran : « Un certificat contesté depuis 2020 »

## Scène 2 — Les faits (0:12–0:42)
Visuel : timeline + icônes de rôles.
- 30 août 2012 : la Cour d'appel de Cotonou nomme Me Lazare CRINOT administrateur (décision n° 28/12).
- 3 avril 2013 : communiqué public de la succession — Me Félix A. BALLEY n'y est mentionné nulle part.
- 20 octobre 2016 : délivrance du certificat d'acquit de droit.
Voix-off (≈ 70 mots) : « Selon le communiqué de la succession du 3 avril 2013, l'administrateur est Me Crinot. Me Balley n'y figure pas. Le 20 octobre 2016, un certificat d'acquit de droit est pourtant délivré, Me Balley y agissant en qualité de mandataire de Gilles Féliho. Celui-ci affirme n'avoir donné aucun mandat. Il conteste aussi la date de décès et l'évaluation des biens. »
Écran (successivement) : « Aucun mandat donné — selon M. Féliho » · « Absent du communiqué de 2013 » · « Mentions contestées : décès, évaluation » (+ renvoi pièce n°)

## Scène 3 — La Cour constitutionnelle (0:42–0:58)
Visuel : texte seul (pas de logo de la Cour) ; extrait du dispositif affiché : « EN CONSEQUENCE, Est incompétente. »
Voix-off : « Le 22 mai 2025, dans sa décision DCC 25-152, la Cour constitutionnelle est saisie de ces faits. Elle se déclare incompétente. Elle ne les écarte pas. Elle ne les infirme pas. C'est aux juridictions ordinaires d'en connaître. »
Écran : « DCC 25-152 — 22 mai 2025 » · « Incompétence. Faits ni écartés, ni infirmés. »

## Scène 4 — La portée (0:58–1:18)
Visuel : carte du Bénin + diaspora, flèches.
Voix-off : « Ce type de situation peut toucher tout héritier éloigné : au Bénin comme dans la diaspora. Savoir qui agit en votre nom dans une succession est un droit à exercer. »
Écran : « Héritiers à l'étranger : vérifiez qui agit en votre nom » (aucune statistique non sourcée)

## Scène 5 — L'appel (1:18–1:40)
Visuel : fond plus lumineux.
Voix-off : « Depuis 2020, M. Féliho demande des explications. Les réponses reçues renvoient vers les juridictions. Il demande que les faits soient examinés. »
Écran : « Sensibiliser. Exiger des comptes. » · « L'intégrité ne se divise pas. »

## Scène 6 — Signature (1:40–fin)
Visuel : nom du site + QR code.
Voix-off : « Les pièces sont en ligne : wadagni2026-verite.com »
Écran : « Sources et pièces justificatives — wadagni2026-verite.com » · #JusticePourFeliho

## À faire avant mise en ligne
- Relire la décision complète : si les observations de l'Agent judiciaire de l'État n'y contestent pas les inexactitudes, ajouter en scène 3 « L'État n'a opposé que l'incompétence et ses diligences ».
- Flouter les données de tiers sur les pièces affichées.
- Héberger hors dépôt (CDN / hébergeur vidéo), `preload="none"`, image d'affiche, sous-titres .vtt, balises Open Graph.
- Corriger de même « Lettre ouverte.pdf » (mention « a confirmé… la réalité des faits »).

## Fichiers produits
- `video/motion-design.mp4` — 1280×720, 24 i/s, 112 s, sous-titres incrustés, piste audio muette (la voix-off reste à enregistrer : texte = sous-titres de chaque scène).
- `video/motion-design.fr.vtt` — sous-titres synchronisés.
- `video/motion.html` + `video/render.js` — source de l'animation et script de rendu (`NODE_PATH=<playwright> node render.js`).

## Révision v3 (116 s) — affirmations fondées sur les pièces
Le texte des sous-titres/voix-off est désormais dans `video/motion.html` (tableau `CUES`) et reprend la transcription de la page d'accueil. Changements : scène 1 et nouvelle scène « Le certificat contre les pièces officielles » (date de décès 10 juin 2016 / acte de décès 3 décembre 2010 ; mandat jamais donné ni produit, y compris devant la BAC le 19 mars 2025 ; valeurs sans rapport avec le jugement) ; scène 3 : DCC 25-152 incompétente, faits ni écartés ni infirmés, observations de l'État limitées à l'incompétence et aux diligences ; scène 5 : art. 39 CPP.

## Révision v4 (116 s) — pièces vérifiées
Sources lues : certificat d'acquit de droit du 20/10/2016 (Direction générale des impôts, service de l'enregistrement : décès « dix juin deux mil seize », Me BALLEY « mandataire », 7 immeubles, 138 300 000 FCFA) ; déclaration de décès CNHU-HKM (décès le 3 décembre 2010) ; jugement n° 114/14 du 31/10/2014 (décès le 3 décembre 2010 ; 39 immeubles France et Bénin estimés à 567 990 000 FCFA ; Me BALLEY non mentionné) ; lettre de Me BALLEY du 7/9/2023 (« actes auxquels il n'est pas partie ») ; sommation du 5/9/2024 (certificat « en date du 20 octobre 2016 »). Phrase sur l'Agent judiciaire supprimée.

## Révision v5 (114 s) — pièces complémentaires
Ajout d'une scène « Les valeurs ne tiennent pas » : lettre AIB du 5/10/2011 (2 tranches de 30 M FCFA de loyer pour 2011, immeuble de Camp Guézo = TF 739, déclaré 65 M dans le certificat) ; titre foncier d'Agla n° 2222 cité au communiqué du 3/4/2013 et absent du certificat (sans lien avec l'écrit manuscrit d'Agla.pdf, qui vise un seul lot) (qui liste les TF 739, 3325, 2601, 786, 123, 158, 1402). L'écrit manuscrit du 12/07/2007 (Agla.pdf) n'est pas chiffré lisiblement : non utilisé à l'écran.

## Révision v6 (114 s) — siège AIB = lot 240 (cachet de la lettre AIB : « 240 Zone Résidentielle » ; certificat, TF 739 : « zone résidentielle, lot 240, Camp Guézo »)
Ajout d'une scène « Les valeurs ne tiennent pas » : lettre AIB du 5/10/2011 (2 tranches de 30 M FCFA de loyer pour 2011, immeuble de Camp Guézo = TF 739, déclaré 65 M dans le certificat) ; titre foncier d'Agla n° 2222 cité au communiqué du 3/4/2013 et absent du certificat (sans lien avec l'écrit manuscrit d'Agla.pdf, qui vise un seul lot) (qui liste les TF 739, 3325, 2601, 786, 123, 158, 1402). L'écrit manuscrit du 12/07/2007 (Agla.pdf) n'est pas chiffré lisiblement : non utilisé à l'écran.

## Révision v7
Le communiqué du 3 avril 2013 est désormais cité comme publié dans le journal La Nation. Tableau d'accueil : mention « plus de 1000 % » remplacée par le montant du jugement.

## Révision v8 (110 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.

## Révision v9 (110 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Tableau « Qui est Me BALLEY » : ajout du successeur de Me Crinot (cabinet repris après son décès), liquidateur sans nom (ordonnance n° 842/2013 et jugement : absent des deux). Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.

## Révision v10 (110 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Tableau « Qui est Me BALLEY » (colonne « Pas Me BALLEY » ; le mot « successeur » n'apparaît qu'une fois, dans la conclusion) : ajout du successeur de Me Crinot (cabinet repris après son décès), liquidateur sans nom (ordonnance n° 842/2013 et jugement : absent des deux). Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.

## Révision v11 (110 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Tableau « Qui est Me BALLEY » (colonne « Pas Me BALLEY » ; le mot « successeur » est supprimé) : ajout du successeur de Me Crinot (cabinet repris après son décès), liquidateur sans nom (ordonnance n° 842/2013 et jugement : absent des deux). Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.

## Révision v12 (127 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Tableau « Qui est Me BALLEY » (colonne « Pas Me BALLEY » ; le mot « successeur » est supprimé ; scène « La portée » rétablie après la conclusion (texte de l'éditeur), puis appel final) : ajout du successeur de Me Crinot (cabinet repris après son décès), liquidateur sans nom (ordonnance n° 842/2013 et jugement : absent des deux). Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.

## Révision v13 (127 s)
La décision DCC 25-152 et les scènes « portée » et « appel » sont retirées. Tableau « Qui est Me BALLEY » (colonne « Pas Me BALLEY » ; le mot « successeur » est supprimé ; conclusion : « Aucun lien juridique prouvé ») : ajout du successeur de Me Crinot (cabinet repris après son décès), liquidateur sans nom (ordonnance n° 842/2013 et jugement : absent des deux). Nouvelle fin : scène « Qui est Me BALLEY dans cette succession ? » (dépositaire du testament, administrateur provisoire, liquidatrice, mandataire : non) puis conclusion (aucun lien juridique ; certificat obtenu « en qualité de mandataire » ; dysfonctionnement très grave ; toujours impuni) et appel final avec l'adresse du site.
