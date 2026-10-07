// Usage : NODE_PATH=<playwright> node render-voix.js <voix.wav> <sortie.mp4>   (ONLY=12,80 pour des images de contrôle)
const {chromium}=require('playwright');const {execSync}=require('child_process');const fs=require('fs'),path=require('path');
const FPS=24,tmp=fs.mkdtempSync(path.join(process.env.TMPDIR||'/tmp','vx-'));
const wav=process.argv[2],out=process.argv[3]||'tiktok-voix.mp4',only=process.env.ONLY?process.env.ONLY.split(',').map(Number):null;
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+path.resolve(__dirname,'motion-voix.html'));await p.evaluate(()=>document.fonts.ready);
 const dur=await p.evaluate(()=>NEWDUR),cues=await p.evaluate(()=>NEWCUES);
 const ts=t=>{const h=String(Math.floor(t/3600)).padStart(2,'0'),m=String(Math.floor(t%3600/60)).padStart(2,'0'),s=(t%60).toFixed(3).padStart(6,'0');return `${h}:${m}:${s}`};
 fs.writeFileSync(path.resolve(__dirname,'tiktok-voix.fr.vtt'),'WEBVTT\n\n'+cues.map((c,i)=>`${i+1}\n${ts(c[0])} --> ${ts(c[1])}\n${c[2]}\n`).join('\n'));
 if(only){for(const t of only){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`./still-${t}.png`});}await b.close();return;}
 for(let i=0;i<dur*FPS;i++){await p.evaluate(t=>seek(t),i/FPS);await p.screenshot({path:`${tmp}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:90});}
 await b.close();
 execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${tmp}/f%05d.jpg -i ${wav} -c:v libx264 -pix_fmt yuv420p -crf 21 -c:a aac -b:a 128k -shortest -movflags +faststart ${out}`);
 fs.rmSync(tmp,{recursive:true});console.log('ok',out);
})();
