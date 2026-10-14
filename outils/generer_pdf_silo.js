// PDF des pages « cas pratique » et « lettres » : NODE_PATH=<playwright> node outils/generer_pdf_silo.js (après construire_silo.py)
const {chromium}=require('playwright');const path=require('path');
const root=path.resolve(__dirname,'..');
const PAGES=[['cas-pratique-plainte-deontologique','cas-pratique-plainte-deontologique','EJI 2.0 — Cas pratique de déontologie'],
             ['lettres-de-demande-de-communication','lettres-de-demande-de-communication','EJI 2.0 — Lettres de demande de communication']];
(async()=>{const b=await chromium.launch({executablePath:process.env.PW_CHROMIUM||'/opt/pw-browsers/chromium'});
for(const [d,f,titre] of PAGES){const dir='batonnier-hounkpatin/'+d;const p=await b.newPage();
await p.goto('file://'+path.join(root,dir,'index.html'),{waitUntil:'load'});
await p.addStyleTag({content:'.cadre{display:none}.droit,.retour,nav.fil{display:none}.wrap{max-width:none}h2.nouvelle-page{break-before:page}blockquote{break-inside:auto}'});
await p.evaluate((d)=>{const q=document.querySelector('article blockquote');if(q&&/Télécharger/.test(q.textContent))q.remove();
 document.querySelectorAll('details').forEach(x=>x.open=true);
 document.querySelectorAll('article h2').forEach(h=>{if(/^Lettre \d/.test(h.textContent))h.classList.add('nouvelle-page')});
 const a=document.querySelector('article');const f=document.createElement('p');f.style.cssText='margin-top:24px;font-size:9pt;color:#555;border-top:1px solid #999;padding-top:6px';
 f.textContent="Source : https://wadagni2026-verite.com/batonnier-hounkpatin/"+d+"/ · Éthique Juridique 2.0 Internationale · version du 14 octobre 2026.";a.appendChild(f);},d);
await p.pdf({path:path.join(root,dir,f+'.pdf'),format:'A4',margin:{top:'16mm',bottom:'16mm',left:'16mm',right:'16mm'},printBackground:true,displayHeaderFooter:true,
 headerTemplate:'<span></span>',footerTemplate:`<div style="font-size:8px;width:100%;text-align:center;color:#555">${titre} — page <span class="pageNumber"></span>/<span class="totalPages"></span></div>`});
console.log('pdf ok',f);}
await b.close();})();
