// PDF du cas pratique : NODE_PATH=<playwright> node outils/generer_pdf_cas_pratique.js (après construire_silo.py)
const {chromium}=require('playwright');const path=require('path'),fs=require('fs');
const root=path.resolve(__dirname,'..');const d='batonnier-hounkpatin/cas-pratique-plainte-deontologique';
(async()=>{const b=await chromium.launch({executablePath:process.env.PW_CHROMIUM||'/opt/pw-browsers/chromium'});const p=await b.newPage();
await p.goto('file://'+path.join(root,d,'index.html'),{waitUntil:'load'});
await p.addStyleTag({content:'.cadre{display:none}.droit,.retour,nav.fil{display:none}.wrap{max-width:none}'});
await p.evaluate(()=>{const q=document.querySelector('article blockquote');if(q&&/Télécharger/.test(q.textContent))q.remove();document.querySelectorAll('details').forEach(x=>x.open=true);
 const a=document.querySelector('article');const f=document.createElement('p');f.style.cssText='margin-top:24px;font-size:9pt;color:#555;border-top:1px solid #999;padding-top:6px';
 f.textContent="Source : https://wadagni2026-verite.com/batonnier-hounkpatin/cas-pratique-plainte-deontologique/ · Éthique Juridique 2.0 Internationale · version du 14 octobre 2026. Cas pratique fondé sur des pièces publiées ; aucune condamnation n'est intervenue à l'encontre des personnes citées.";a.appendChild(f);});
await p.pdf({path:path.join(root,d,'cas-pratique-plainte-deontologique.pdf'),format:'A4',margin:{top:'16mm',bottom:'16mm',left:'16mm',right:'16mm'},printBackground:true,displayHeaderFooter:true,
 headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#555">EJI 2.0 — Cas pratique de déontologie — page <span class="pageNumber"></span>/<span class="totalPages"></span></div>'});
await b.close();console.log('pdf ok');})();
