def arrow(a, b, x, y): text("→", x, y, 80, a, b, 'bigtext ocre')
def qcard(src, date, html, x, y, w, a, b):   # citation typée d'une pièce (courriel), avec sa source
    el(f'<div class="mail"><div class="mh">{src}<span>{date}</span></div>{html}</div>', a, b, 0.5, 'piece', f'left:{x}px;top:{y}px;width:{w}px')

el("Ce film présente des pièces publiées sur le site : jugement, procès-verbal, convocations, lettres, plainte déontologique. Aucune infraction n'est imputée par ce film ; les qualifications relèvent des juridictions. Droit de réponse ouvert à Me Fade, à l'Ordre et au parquet général.", 0, TOTAL, 0.6, 'bandeau')

# --- 1 : le constat sans acte
a, b = Q(1); W1 = [W(1, i) for i in range(3)]
text("31 OCTOBRE 2014 · LE JUGEMENT N° 114/14", 80, 62, 1760, a + 0.3, b, 'colhead wide')
pic('j8c.png', 80, 140, 840, a + 0.4, W1[1][0] - 0.3, "Jugement n° 114/14/3ᵉ CH-EP du 31 octobre 2014, dispositif", h=640, cls='f1')
pic('j5c.png', 80, 140, 840, W1[1][0] - 0.3, b, "Jugement, p. 5 : « a même déjà disposé de cet immeuble »", h=640, cls='f1')
text("« Constate que Gilles Sixte Féliho <b>a exécuté les dispositions testamentaires de manière volontaire</b> »", 1000, 150, 840, W1[0][0] - 0.2, b, 'quote')
text("« Que Gilles Sixte Féliho <b>a même déjà disposé de cet immeuble</b> » : la parcelle bâtie du lot 488", 1000, 330, 840, W1[1][0] - 0.2, b, 'quote')
text("<div class='pulse qa'>QUEL ACTE ?</div>", 1000, 520, 840, W1[2][0] - 0.2, b, '')
text("Le jugement n'en cite aucun.", 1000, 740, 840, W1[2][0] + 1.6, b, 'nm ocrebox')

# --- 2 : l'huissier, les registres
a, b = Q(2); W2 = [W(2, i) for i in range(3)]
heads(a + 0.2, b, 'PROCÈS-VERBAL DE COMPULSION', 'CE QUE RÉPONDENT LES REGISTRES')
pic('pvc1c.png', 80, 140, 840, a + 0.4, W2[1][0] - 0.3, "Procès-verbal de compulsion du 19 décembre 2017, p. 1", h=640, cls='f2')
pic('pvc2c.png', 80, 140, 840, W2[1][0] - 0.3, b, "Procès-verbal de compulsion, p. 2 : mairie de Cotonou, « superficie : néant »", h=640, cls='f2')
card(19, 'DÉC.', 2017, 1000, 150, W2[0][0] - 0.2, b, 'big', 'compulsion')
text("« Qu'en réalité, il n'a <b>jamais aliéné</b> à quelque titre que ce soit ladite parcelle »", 1450, 170, 420, W2[0][0] + 0.8, b, 'ctext')
text("Mairie de Cotonou · superficie : <b>néant</b>", 1000, 560, 840, W2[1][0] - 0.2, b, 'nm')
text("Institut géographique national · <b>aucun document</b>", 1000, 660, 840, W2[1][0] + 2.4, b, 'nm')
text("Soit quelqu'un a vendu à sa place.<br>Soit la parcelle n'existe pas.", 1000, 790, 840, W2[2][0] + 1.0, b, 'bigtext')

# --- 3 : qui a invoqué la vente
a, b = Q(3); W3 = [W(3, i) for i in range(4)]
heads(a + 0.2, b, 'LES PARTIES ET LEUR AVOCAT', 'QUI A ALLÉGUÉ LA VENTE ?')
pic('j1c.png', 80, 140, 840, a + 0.4, W3[2][0] - 0.3, "Jugement, p. 1 : « tous assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f3')
pic('j4c.png', 80, 140, 840, W3[2][0] - 0.3, b, "Jugement, p. 4 : les conclusions des héritiers", h=640, cls='f3')
text("<b>Les héritiers</b>, dans leurs conclusions", 1000, 150, 840, W3[0][0] - 0.2, b, 'quote')
text("<b>Assistés de Me Victorien Olatundji Fade</b>, avocat à la Cour", 1000, 270, 840, W3[1][0] - 0.2, b, 'quote ocrebox')
text("Conclusions des héritiers : quartier <b>Godomey</b>", 1000, 440, 840, W3[2][0] - 0.2, b, 'nm')
text("Jugement : quartier <b>Gbégamey</b>", 1000, 540, 840, W3[3][0] - 0.2, b, 'nm')
text("Procès-verbal de 2017 : lotissement de <b>Gbégamey</b>", 1000, 640, 840, W3[3][0] + 1.4, b, 'nm')
text("Deux quartiers pour une seule parcelle.", 1000, 780, 840, W3[3][0] + 3.0, b, 'bigtext')

# --- 4 : l'acte, s'il existe
a, b = Q(4); W4 = [W(4, i) for i in range(5)]
text("L'ACTE DE DISPOSITION", 80, 62, 840, a + 0.2, b, 'colhead'); text("QUI PEUT LE PRODUIRE ?", 1000, 62, 840, a + 0.2, b, 'colhead')
el('', a, b, 0.5, 'vbar', 'left:959px;top:56px;height:880px')
FR = ('<div style="width:840px;height:760px;border:5px dashed rgba(199,210,254,.5);border-radius:14px;padding:30px 36px;font:700 34px DejaVu Serif;color:#e2e8f0;line-height:1.3">'
      'ACTE DE DISPOSITION<br><span style="font-size:26px;color:#94a3b8;font-weight:400">de la parcelle B du lot 488, après le décès du 3 décembre 2010</span></div>')
el(FR, a + 0.3, b, 0.6, '', 'left:80px;top:140px;width:840px;height:760px')
for i, (lb, ta) in enumerate([("DATE", W4[3][0] - 0.2), ("OFFICIER", W4[3][0] + 0.9), ("ACQUÉREUR", W4[3][0] + 1.8)]):
    text(f"<span style='color:#94a3b8;font-size:30px'>{lb}</span> <span class='qa' style='font-size:90px'>?</span>", 120, 330 + i * 170, 760, ta, b, '')
text("Avocat obligatoire : <b>seuls les avocats des parties déposent les pièces</b>", 1000, 150, 840, W4[0][0] - 0.2, b, 'quote')
text("Ces pièces sont <b>débattues contradictoirement</b>", 1000, 300, 840, W4[1][0] - 0.2, b, 'quote')
text("Si l'acte existe, <b>il est entre les mains de Me Fade</b>", 1000, 430, 840, W4[2][0] - 0.2, b, 'quote ocrebox')
text("Qu'il le montre.", 1000, 590, 840, W4[3][0] - 0.2, b, 'bigtext')
counter(4368, 'JOURS', 1000, 690, W4[4][0] - 0.2, b, W4[4][0], W4[4][0] + 3.2, w=840, size=120, sub="du 31 octobre 2014 au 16 octobre 2026 : aucun acte montré au plaignant")

# --- 5 : mandataire, puis adversaire
a, b = Q(5); W5 = [W(5, i) for i in range(5)]
heads(a + 0.2, b, 'LES PIÈCES', 'DE MANDATAIRE À ADVERSAIRE')
pic('gang.png', 80, 140, 840, a + 0.4, W5[1][0] - 0.3, "Lettre du notaire Gangnito à Me Fade, 19 septembre 2007", h=640, cls='f5')
qcard("Courriels de Lise Féliho, août 2007", "« a/s ta maison »", "<p>« je voulais confier ça à FADE et tu as refusé »</p><p>« maîtrisant le dossier pour l'avoir suivi à son début, il fera l'affaire »</p>", 80, 160, 840, W5[1][0] - 0.3, W5[2][0] - 0.3)
pic('cd1.png', 80, 140, 840, W5[2][0] - 0.3, W5[2][1] + 3.0, "Citation directe, 4 et 7 juin 2013 : héritiers « assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f5')
pic('cd5.png', 80, 140, 840, W5[2][1] + 3.0, W5[3][0] - 0.3, "Citation directe, p. 5 : Gilles Féliho « complice du délit de diffamation »", h=640, cls='f5')
pic('j1c.png', 80, 140, 840, W5[3][0] - 0.3, W5[3][0] + 4.2, "Jugement du 31 octobre 2014 : « tous assistés de Maître Victorien Olatoundji Fade »", h=640, cls='f5')
pic('sig.png', 80, 140, 840, W5[3][0] + 4.2, b, "Signification du jugement, 9 mars 2015 : « tous assistés de Maître Victorien O. Fade »", h=640, cls='f5')
card(19, 'SEPT.', 2007, 1000, 150, W5[0][0] - 0.2, b, 'sm', 'mandataire')
card(4, 'JUIN', 2013, 1290, 150, W5[2][0] - 0.2, b, 'sm', 'citation directe')
card(31, 'OCT.', 2014, 1000, 430, W5[3][0] - 0.2, b, 'sm', 'jugement')
card(9, 'MARS', 2015, 1290, 430, W5[3][0] + 3.6, b, 'sm', 'signification')
text("Le mandataire d'hier,<br><span class='ocre'>l'adversaire d'aujourd'hui.</span>", 1000, 740, 840, W5[4][0] - 0.2, b, 'bigtext')

# --- 6 : la règle
a, b = Q(6); W6 = [W(6, i) for i in range(4)]
heads(a + 0.2, b, 'LA RÈGLE ÉCRITE', 'LA PLAINTE DÉONTOLOGIQUE')
pic('ri12.png', 80, 140, 840, a + 0.4, W6[2][0] - 0.3, "Règlement intérieur harmonisé des barreaux de l'espace UEMOA (5 mai 2023), art. 24.1", h=640, cls='f6')
pic('pd.png', 80, 140, 840, W6[2][0] - 0.3, b, "Plainte déontologique au Bâtonnier, 2 avril 2023, p. 1 (coordonnées occultées)", h=640, cls='f6')
text("« […] ne peut accepter l'affaire d'un nouveau client […] lorsque la connaissance par l'avocat des affaires de <b>l'ancien client favoriserait le nouveau client</b> »", 1000, 150, 840, W6[0][0] - 0.2, b, 'quote')
text("« ne peut être ni le conseil ni le représentant ou le défenseur <b>de plus d'un client dans une même affaire</b> »", 1000, 400, 840, W6[1][0] - 0.2, b, 'quote')
card(2, 'AVR.', 2023, 1000, 150, W6[2][0] - 0.2, b, 'sm', 'plainte déontologique')
text("<b>Complicité</b> de faux en écriture publique<br><b>Usage</b> de faux en écriture publique<br><span class='cap2'>articles 303 à 305 et 22 du Code pénal, tels que cités dans la plainte</span>", 1000, 430, 840, W6[3][0] - 0.2, b, 'quote ocrebox')

# --- 7 : la convocation qu'on ne peut pas ignorer
a, b = Q(7); W7 = [W(7, i) for i in range(5)]
heads(a + 0.2, b, 'CONVOQUÉ, NON PRÉSENTÉ', 'CE QUE DISENT LES PIÈCES')
pic('conv.png', 80, 140, 840, a + 0.4, W7[2][0] - 0.3, "Brigade criminelle, convocation n° 141/DGPR/DPJ/BC/2025", h=640, cls='f7')
pic('bat.png', 80, 140, 840, W7[2][0] - 0.3, W7[3][0] - 0.3, "Le Bâtonnier au procureur général, 17 mars 2025", h=640, cls='f7')
pic('rel.png', 80, 140, 840, W7[3][0] - 0.3, b, "Brigade criminelle, 25 mars 2025 : « il ne s'est pas présenté »", h=640, cls='f7')
card(12, 'MARS', 2025, 1000, 150, W7[0][0] - 0.2, b, 'sm', 'convocation')
arrow(W7[0][0] + 1.0, b, 1265, 190); card(19, 'MARS', 2025, 1340, 150, W7[0][0] + 1.0, b, 'sm', 'comparution')
text("<b>Art. 56 du Code de procédure pénale</b> : « les personnes convoquées sont tenues de comparaître […] elles peuvent y être contraintes par la force publique »", 1000, 430, 840, W7[1][0] - 0.2, b, 'quote ocrebox')
text("17 mars · le Bâtonnier : « prérogative de consultation »", 1000, 650, 840, W7[2][0] - 0.2, b, 'nm')
text("19 mars · « il ne s'est pas présenté »<br>Le notaire est entendu de 9 h 14 à 10 h 52", 1000, 750, 840, W7[3][0] - 0.2, b, 'nm')
text("Une convocation <span class='ocre'>oblige</span>.<br>Une invitation, non.", 1000, 870, 840, W7[4][0] - 0.2, b, 'bigtext')

# --- 8 : l'Ordre et le procureur général
a, b = Q(8); W8 = [W(8, i) for i in range(5)]
heads(a + 0.2, b, 'LA LOI SUR LE BARREAU (1965)', 'CE QUI S\'EST PASSÉ')
pic('l65b.png', 80, 140, 840, W8[1][0] - 0.3, b, "Loi sur le barreau (avril 1965), art. 30 : plaintes transmises, délais de trois mois, saisine directe de la Cour d'appel", h=640, cls='f8')
card(2, 'AVR.', 2023, 80, 160, a + 0.4, W8[1][0] - 0.3, 'big', 'plainte déontologique')
text("20 juin 2024 · relance au Bâtonnier<br><b>aucune décision connue</b>", 560, 220, 360, W8[0][0] + 1.6, W8[1][0] - 0.3, 'ctext')
text("Art. 30 : <b>trois mois</b> sans décision du conseil de discipline → le procureur général <b>peut saisir directement la Cour d'appel</b>", 1000, 150, 840, W8[1][0] - 0.2, b, 'quote')
text("14 mars 2025 · le procureur général écrit au Bâtonnier<br>17 mars · « la cause est déjà en instruction »", 1000, 400, 840, W8[2][0] - 0.2, b, 'nm')
counter(1293, 'JOURS', 1000, 520, W8[3][0] - 0.2, b, W8[3][0], W8[3][0] + 2.4, w=840, size=100, sub="depuis la plainte déontologique du 2 avril 2023")
counter(581, 'JOURS', 1000, 700, W8[3][0] + 1.6, b, W8[3][0] + 2.0, W8[3][0] + 4.0, w=840, size=100, sub="depuis la lettre du procureur général du 14 mars 2025")
text("Le pouvoir existe.<br><span class='ocre'>Qui l'exerce ?</span>", 1000, 890, 840, W8[4][0] - 0.2, b, 'bigtext')

# --- 9 : les questions
a, b = Q(9); W9 = [W(9, i) for i in range(4)]
QS = [("À ME FADE", "Où est <b>l'acte de disposition</b> ? Quelle date, quel officier, quel acquéreur ?"),
      ("À ME FADE", "Pourquoi ne pas vous être présenté <b>à la convocation</b> de la Brigade criminelle ?"),
      ("AU BÂTONNIER", "Où est <b>la décision</b> sur la plainte du 2 avril 2023 ?"),
      ("AU PROCUREUR GÉNÉRAL", "Pourquoi ne pas <b>saisir la Cour d'appel</b> ?")]
for i, (who, q) in enumerate(QS):
    text(f"<span class='colhead'>{who}</span><br><span class='bigq'>{q}</span>", 160, 150 + i * 200, 1600, W9[i][0] - 0.2, b, 'quest')

# --- 10 : conclusion
a, b = Q(10); W10 = [W(10, i) for i in range(3)]
text("Une seule pièce suffit.", 80, 260, 1760, W10[0][0] - 0.2, b, 'title2')
text("<span class='ocre'>Si l'acte existe, qu'il le montre.</span>", 80, 440, 1760, W10[1][0] - 0.2, b, 'title2')
text("Tant qu'il ne le montre pas, le constat du jugement repose<br>sur un acte que personne n'a vu.", 80, 640, 1760, W10[2][0] - 0.2, b, 'quote ocretext')
text("Gilles Sixte Féliho — plaignant", 80, 840, 1760, W10[2][0] + 2.0, b, 'ctext')

# --- carton final
a, b = SQ[16]
text('wadagni2026-verite.com', 0, 300, 1920, a + 0.6, b, 'url', 0.8)
text('Les pièces reproduites dans ce film sont publiées sur le site, avec leurs empreintes numériques.', 0, 400, 1920, a + 1.6, b, 'finsmall', 0.8)
text("Les extraits reproduits sont des copies partielles ; les coordonnées personnelles sont occultées. Les articles sont ceux qui figurent dans les pièces, dans la loi d'avril 1965 sur le barreau et dans le règlement intérieur harmonisé des barreaux de l'UEMOA (5 mai 2023, postérieur aux faits de 2007 à 2015). "
     "Le règlement intérieur du Barreau du Bénin n'est pas publié ici. Le dossier, l'acte de disposition et les points d'interrogation sont des illustrations.", 160, 560, 1600, a + 2.6, b, 'precis', 0.8)

