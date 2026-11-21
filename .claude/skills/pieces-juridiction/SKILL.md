---
name: pieces-juridiction
description: Règle absolue pour toute pièce destinée à une juridiction, à une autorité judiciaire ou à une partie adverse (assignation, sommation, requête, bordereau, plainte, demande amiable) : ne jamais flouter, noircir ni occulter une pièce. À lire avant de tamponner, assembler ou verser une pièce.
---

# Pièces destinées à une juridiction : jamais de floutage

**Règle de l'éditeur (Gilles Féliho, 20 novembre 2026).** On ne floute jamais une pièce destinée à une juridiction. Aucune occultation, aucun rectangle noir, aucun masquage de nom, d'adresse, de téléphone, de filiation ou de courriel.

## Pourquoi
- Une pièce occultée n'est plus la pièce : le juge et l'adversaire peuvent y voir une altération, et elle perd sa force probante.
- Le tampon « PIÈCE N° » est une **bande ajoutée autour** de la page (voir `outils/tamponner_pieces.py`), jamais une surcharge qui couvre du contenu.

## Les versions publiées sur le site sont occultées : ne pas les prendre
Les PDF du dépôt servis par le site (silo, pages publiques) ont été occultés pour la diffusion publique (adresses, téléphones, filiation). Ce sont des **versions de diffusion**, pas des pièces de procédure. Pour une pièce de juridiction, remonter à la **version sans occultation** :
1. le scan fourni par l'éditeur (dossier d'envois de la session) ;
2. à défaut, la **première version** du fichier dans l'historique git (`git log --follow -- <fichier>` puis `git show <commit>:<fichier>`) : les occultations ont été ajoutées après coup, souvent à la mi-octobre 2026 ;
3. à défaut, demander l'original à l'éditeur. Ne jamais livrer la version occultée « faute de mieux » sans le dire.

## Contrôle avant toute remise
Lancer `python3 -I outils/verifier_pieces_juridiction.py <fichier.pdf> ...` : il signale les aplats noirs opaques vectoriels. Il ne voit pas une occultation incorporée dans l'image : regarder aussi chaque première page (rendu à l'œil).

## Annotations d'origine
Les annotations portées par les scans (« Pièce n°9 », « H1 », surlignages) ne sont pas des occultations : ne pas les gommer sans demande de l'éditeur, mais signaler celles qui contredisent la numérotation de l'acte.
