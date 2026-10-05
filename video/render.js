// Usage: NODE_PATH=<playwright> node render.js [out.mp4]
// Rend motion.html image par image (24 fps) puis encode en MP4 + écrit les sous-titres .vtt
const {chromium}=require('playwright');const {execSync}=require('child_process');const fs=require('fs'),path=require('path');
const FPS=24, tmp=fs.mkdtempSync(path.join(process.env.TMPDIR||'/tmp','mo-'));
const out=process.argv[2]||'motion-design.mp4', only=process.env.ONLY?process.env.ONLY.split(',').map(Number):null;
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:720}});
 await p.goto('file://'+path.resolve('motion.html'));await p.evaluate(()=>document.fonts.ready);
 const dur=await p.evaluate(()=>DUR),cues=await p.evaluate(()=>CUES);
 const ts=t=>{const h=String(Math.floor(t/3600)).padStart(2,'0'),m=String(Math.floor(t%3600/60)).padStart(2,'0'),s=(t%60).toFixed(3).padStart(6,'0');return `${h}:${m}:${s}`};
 fs.writeFileSync('motion-design.fr.vtt','WEBVTT\n\n'+cues.map((c,i)=>`${i+1}\n${ts(c[0])} --> ${ts(c[1])}\n${c[2]}\n`).join('\n'));
 if(only){for(const t of only){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`still-${t}.png`});}await b.close();return;}
 for(let i=0;i<dur*FPS;i++){await p.evaluate(t=>seek(t),i/FPS);await p.screenshot({path:`${tmp}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
 await b.close();
 execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${tmp}/f%05d.jpg -f lavfi -i anullsrc=r=44100:cl=stereo -shortest -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -movflags +faststart ${out}`);
 fs.rmSync(tmp,{recursive:true});console.log('ok',out);
})();
