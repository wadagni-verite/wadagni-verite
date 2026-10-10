"""Appose le tampon « PIÈCE N°x » (modèle bleu de la plainte déontologique) sur un PDF ou une image,
sans masquer le document : une bande est ajoutée en haut et en bas de chaque page.
Usage : python3 -I outils/tamponner_pieces.py <source.pdf|image> <sortie.pdf> <numéro> "<intitulé>" """
import sys, pymupdf
NAVY=(0.11,0.20,0.50); RED=(0.78,0.09,0.12); INK=(0.08,0.08,0.10); WHITE=(1,1,1); PALE=(0.82,0.87,0.97)
L1="Plainte déontologique - Notaire Félix A. BALLEY"; L2="Succession J. F. FELIHO"
TOP1,TOP2,BOT=112,32,28

def _wrap(txt,font,size,maxw):
    out,cur=[],""
    for w in txt.split():
        t=(cur+" "+w).strip()
        if pymupdf.get_text_length(t,fontname=font,fontsize=size)<=maxw: cur=t
        else: out.append(cur); cur=w
    return out+[cur]

def _source(src):
    if src.lower().endswith(".pdf"): return pymupdf.open(src)
    img=pymupdf.open(src); pdf=pymupdf.open("pdf",img.convert_to_pdf()); return pdf

def stamp(src,dst,num,titre):
    s=_source(src); n=len(s); out=pymupdf.open()
    for i,sp in enumerate(s):
        r=sp.rect; top=TOP1 if i==0 else TOP2
        p=out.new_page(width=r.width,height=r.height+top+BOT)
        p.show_pdf_page(pymupdf.Rect(0,top,r.width,top+r.height),s,i,rotate=-sp.rotation)
        W=r.width
        if i==0:
            x0,y0,w=36,10,min(360,W-72); hbar=36; hbody=top-y0-hbar-10
            p.draw_rect(pymupdf.Rect(x0,y0,x0+w,y0+hbar),color=NAVY,fill=NAVY)
            p.insert_text((x0+10,y0+16),L1,fontsize=11.5,fontname="hebo",color=WHITE)
            p.insert_text((x0+10,y0+30),L2,fontsize=9.5,fontname="helv",color=PALE)
            p.draw_rect(pymupdf.Rect(x0,y0+hbar,x0+w,y0+hbar+hbody),color=NAVY,width=1.6)
            p.insert_text((x0+10,y0+hbar+27),f"PIÈCE N°{num}",fontsize=21,fontname="hebo",color=RED)
            lines=_wrap("· "+titre,"hebo",9.5,w-20)[:3]
            for k,l in enumerate(lines): p.insert_text((x0+10,y0+hbar+42+k*11.5),l,fontsize=9.5,fontname="hebo",color=INK)
        else:
            p.insert_text((36,20),f"PIÈCE N°{num}",fontsize=10,fontname="hebo",color=RED)
            p.insert_text((36+pymupdf.get_text_length(f"PIÈCE N°{num}",fontname="hebo",fontsize=10)+10,20),"· "+titre[:90],fontsize=8.5,fontname="hebo",color=NAVY)
        f=f"{L1} · {L2} · Pièce n°{num} · page {i+1}/{n}"
        tw=pymupdf.get_text_length(f,fontname="helv",fontsize=7.5)
        p.draw_line((36,r.height+top+6),(W-36,r.height+top+6),color=NAVY,width=.6)
        p.insert_text(((W-tw)/2,r.height+top+18),f,fontsize=7.5,fontname="helv",color=NAVY)
    out.set_metadata({"title":f"Pièce n°{num} — {titre}","author":"Gilles FÉLIHO — wadagni2026-verite.com","subject":"Plainte déontologique - Notaire Félix A. BALLEY - Succession J. F. FELIHO"})
    out.save(dst,garbage=4,deflate=True)
if __name__=="__main__": stamp(*sys.argv[1:5])
