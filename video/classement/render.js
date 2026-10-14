// Usage : NODE_PATH=<playwright> node render.js <audio.wav> <sortie.mp4>      (ONLY=3,20,55 : images de contrôle still-*.png)
const {chromium}=require('playwright');const {execSync}=require('child_process');const fs=require('fs'),path=require('path');
const FPS=24,tmp=fs.mkdtempSync(path.join(process.env.TMPDIR||'/tmp','cl-'));
const wav=process.argv[2],out=process.argv[3]||'film.mp4',only=process.env.ONLY?process.env.ONLY.split(',').map(Number):null;
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+path.resolve(__dirname,'motion.html'));await p.evaluate(()=>document.fonts.ready);
 if(only){for(const t of only){await p.evaluate(t=>seek(t),t);await p.screenshot({path:path.resolve(__dirname,`still-${t}.png`)});}await b.close();return;}
 const dur=await p.evaluate(()=>TOTAL);
 for(let i=0;i<dur*FPS;i++){await p.evaluate(t=>seek(t),i/FPS);await p.screenshot({path:`${tmp}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
 await b.close();
 execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${tmp}/f%05d.jpg -i ${wav} -c:v libx264 -preset medium -b:v 10M -maxrate 12M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart ${out}`);
 fs.rmSync(tmp,{recursive:true});console.log('ok',out);
})();
