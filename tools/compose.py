import os, numpy as np
from PIL import Image
from scipy import ndimage as ndi
base='/mnt/user-data/uploads/SP NAP DRIVE'
def cut(path,rot=0):
    im=Image.open(path).convert('RGB')
    if rot: im=im.rotate(-rot,expand=True)
    im.thumbnail((1100,1100))
    a=np.asarray(im).astype(float); mn=a.min(axis=2)
    nw=mn>=250; lab,k=ndi.label(nw); sizes=ndi.sum(nw,lab,range(1,k+1))
    bg=np.isin(lab,[i+1 for i,s in enumerate(sizes) if s>4000]); fg=ndi.binary_opening(~bg,iterations=2)
    l2,k2=ndi.label(fg); s2=ndi.sum(fg,l2,range(1,k2+1)); fg=l2==(1+int(np.argmax(s2)))
    fg=ndi.binary_erosion(fg,iterations=5)
    alpha=ndi.gaussian_filter(fg.astype(float),1.0)
    g=a.mean(axis=2)/255
    # lam deu: bu phan sang toi dien rong (low-frequency) trong vung san pham, giu chi tiet
    m=ndi.gaussian_filter(fg.astype(float),60)+1e-6
    low=ndi.gaussian_filter(g*fg,60)/m
    target=(g*fg).sum()/max(fg.sum(),1)
    g2=np.clip(g+0.6*(target-low),0,1)
    out=np.clip(g2**0.72,0,1)*255
    ys,xs=np.where(fg)
    rgba=np.dstack([out]*3+[alpha*255]).astype(np.uint8)[max(0,ys.min()-6):ys.max()+7,max(0,xs.min()-6):xs.max()+7]
    return Image.fromarray(rgba,'RGBA')
PAIRS={'KS500RK':[('KS500RK/10',0),('KS500RK/43',0)],'KS500LK':[('KS500LK/25',0),('KS500RK/55',0)],
'KS11':[('KS11/25',0),('KS11/10',0)],'KS09':[('KS09/11',90),('KS09/INAX_2',0)],'KS609TC':[('KS609TC/2',0),('KS609TC/22',0)],
'KS15U':[('KS15U/9',0),('KS15U/19',0)],'KS005':[('KS005/4',0),('KS005/8',0)],'KS21':[('KS21/7',0),('KS21/29',0)],
'KS504C':[('KS504C/2',0),('KS504C/4',0)],'KS45':[('KS45/4',0),('KS45/8',0)],'KS602K':[('KS602K/8',0),('KS602K/11',0)],'KS608U':[('KS608U/4',0),('KS608U/17',0)]}
if __name__=='__main__':
    for code,items in PAIRS.items():
        ims=[cut(f'{base}/{f}.png',rot) for f,rot in items]
        H=620; ims=[im.resize((max(1,int(im.width*H/im.height)),H)) for im in ims]
        gap=40; W=sum(i.width for i in ims)+gap*(len(ims)-1)+20
        cv=Image.new('RGBA',(W,H+20),(0,0,0,0)); x=10
        for im in ims: cv.alpha_composite(im,(x,10)); x+=im.width+gap
        cv.save(f'img/{code}_pair.png'); print(code,cv.size)
