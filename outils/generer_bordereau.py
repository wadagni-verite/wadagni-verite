"""Génère la section « Bordereau des pièces » de index.html et l'archive ZIP à partir de pieces/bordereau/.
Usage : python3 -I outils/generer_bordereau.py   (à relancer après l'ajout de nouvelles pièces)"""
import glob, os, re, zipfile, html, pymupdf
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITRES={1:"Certificat de décès de feu Jean Florentin FELIHO",2:"PV de Lecture du Testament olographe (24/04/2012)",
3:"Courriel officiel de l'Étude Irène ADJAGBA ICHOLA",4:"Communiqué de l'Administrateur judiciaire (La Nation)",
5:"Jugement civil contradictoire n°114/14 du TPI de Cotonou",6:"Certificat d'Acquit de Droit frauduleux (20/10/2016)",
7:"Lettre officielle d'observations de la DGI (06/01/2025)",8:"Sommation interpellative et de compulsion d'huissier",
9:"Lettre de réponse de Me Félix BALLEY (07/09/2023)",10:"Procès-verbal de séance de l'APDP (19/06/2024)",
11:"Audition de témoin de Me BALLEY (Brigade Criminelle)",12:"Constat d'huissier avec interpellation (Immeuble VISSIM)",
13:"PV de compulsion foncière Mairie de Cotonou & IGN",14:"Lettre de transmission foncière de 2007 (Lot 923)",
15:"Contestation formelle et mise en demeure à la DGI"}
D=os.path.join(ROOT,'pieces','bordereau')
fich={}
for f in sorted(glob.glob(os.path.join(D,'piece-*.pdf'))):
    fich[int(re.match(r'piece-(\d+)-',os.path.basename(f)).group(1))]=f
rows=[]
for n in sorted(fich):
    f=fich[n]; pg=len(pymupdf.open(f)); ko=os.path.getsize(f)/1024
    taille=f"{ko/1024:.1f} Mo" if ko>=1024 else f"{ko:.0f} Ko"
    rel=os.path.relpath(f,ROOT).replace(os.sep,'/')
    rows.append(f'''                        <tr><td class="bd-num">{n}</td><td>{html.escape(TITRES[n])}</td><td class="bd-meta">{pg}&nbsp;p. · {taille}</td><td><a class="bd-btn" href="{rel}" download>📥 Télécharger la pièce n°{n}</a></td></tr>''')
zp=os.path.join(D,'bordereau-pieces-tamponnees.zip')
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
    for n in sorted(fich): z.write(fich[n],os.path.basename(fich[n]))
zko=os.path.getsize(zp)/1024/1024
sect=f'''<!-- BORDEREAU:START -->
    <section class="bordereau" id="bordereau">
        <div class="container">
            <h2>Bordereau des pièces</h2>
            <p class="bd-sub">Plainte déontologique — Notaire Félix A. BALLEY — Succession J. F. FELIHO. {len(fich)} pièces numérotées, chacune téléchargeable individuellement et revêtue de son tampon.</p>
            <div class="bd-wrap">
                <table class="bd-table">
                    <thead><tr><th>N°</th><th>Intitulé</th><th>Format</th><th>Téléchargement</th></tr></thead>
                    <tbody>
{chr(10).join(rows)}
                    </tbody>
                </table>
            </div>
            <p class="bd-all"><a class="bd-btn bd-btn-all" href="pieces/bordereau/bordereau-pieces-tamponnees.zip" download>📦 Télécharger toutes les pièces (ZIP, {zko:.1f} Mo)</a></p>
        </div>
    </section>
<!-- BORDEREAU:END -->'''
css='''        /* Bordereau des pièces */
        .bordereau { padding: 50px 20px; background: var(--light-gray); }
        .bordereau h2 { text-align: center; color: var(--navy); font-size: 1.9rem; margin-bottom: 8px; }
        .bd-sub { text-align: center; color: var(--gray); max-width: 760px; margin: 0 auto 26px; }
        .bd-wrap { overflow-x: auto; border-radius: 12px; box-shadow: 0 4px 18px rgba(10,31,68,.08); }
        .bd-table { width: 100%; min-width: 680px; border-collapse: collapse; background: #fff; font-size: .95rem; }
        .bd-table th { background: #1c3380; color: #fff; text-align: left; padding: 12px 14px; font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; }
        .bd-table td { padding: 12px 14px; border-top: 1px solid #e5e7eb; vertical-align: middle; }
        .bd-num { font-weight: 800; color: #c7171f; font-size: 1.15rem; text-align: center; width: 54px; }
        .bd-meta { color: var(--gray); white-space: nowrap; font-size: .85rem; }
        .bd-btn { display: inline-block; background: #1c3380; color: #fff; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-weight: 600; font-size: .85rem; white-space: nowrap; }
        .bd-btn:hover { background: var(--navy); }
        .bd-all { text-align: center; margin-top: 22px; }
        .bd-btn-all { background: var(--gold); color: var(--navy); padding: 12px 22px; font-size: 1rem; }
        .bd-btn-all:hover { background: #c19b2e; }
'''
p=os.path.join(ROOT,'index.html'); s=open(p,encoding='utf-8').read()
if '/* Bordereau des pièces */' not in s:
    a='        .video-section {'
    assert s.count(a)==1; s=s.replace(a,css+a,1)
if '<!-- BORDEREAU:START -->' in s:
    s=re.sub(r'<!-- BORDEREAU:START -->.*?<!-- BORDEREAU:END -->',lambda m:sect,s,flags=re.S)
else:
    i=s.index('id="video-avocat"'); j=s.index('</section>',i)+len('</section>')
    s=s[:j]+'\n\n    '+sect+s[j:]
open(p,'w',encoding='utf-8').write(s); print(len(fich),'pièces ; ZIP',round(zko,1),'Mo')
