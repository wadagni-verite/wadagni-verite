// Génère les images Open Graph 1200x630 du silo : NODE_PATH=<playwright> node outils/generer_og_silo.js
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');const pages=JSON.parse(fs.readFileSync(path.join(root,'outils/silo/pages.json'),'utf8'));
fs.mkdirSync(path.join(root,'batonnier-hounkpatin/og'),{recursive:true});
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
(async()=>{const b=await chromium.launch({executablePath:process.env.PW_CHROMIUM||'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1200,height:630}});
for(const [url,title,desc,slug,h1] of pages){const name=url==='/batonnier-hounkpatin/'?'dossier':slug;
 await p.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:linear-gradient(135deg,#0a1f44,#1e3a8a);font-family:'DejaVu Serif',Georgia,serif;color:#fff;position:relative;overflow:hidden">
 <div style="position:absolute;left:0;right:0;top:0;height:10px;background:#d4af37"></div>
 <div style="position:absolute;left:70px;top:70px;font:700 24px 'DejaVu Sans',Arial;letter-spacing:.14em;text-transform:uppercase;color:#d4af37">Dossier institutionnel · EJI 2.0</div>
 <div style="position:absolute;left:70px;right:70px;top:150px;font-size:56px;line-height:1.25;font-weight:700">${esc(h1)}</div>
 <div style="position:absolute;left:70px;bottom:62px;font:400 28px 'DejaVu Sans',Arial;color:#cbd5e1">Les pièces, rien que les pièces · wadagni2026-verite.com</div>
 <div style="position:absolute;left:0;right:0;bottom:0;height:10px;background:#d4af37"></div></body></html>`);
 await p.screenshot({path:path.join(root,'batonnier-hounkpatin/og',name+'.jpg'),type:'jpeg',quality:84});}
await b.close();console.log('og ok');})();
