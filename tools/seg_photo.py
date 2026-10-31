import numpy as np
from PIL import Image
from scipy import ndimage as ndi
def seg(path,rot=0,out=None,fill_all=False,close_it=6,sat_th=0.16,v_th=0.58):
    im=Image.open(path).convert('RGB')
    if rot: im=im.rotate(rot,expand=True)
    im.thumbnail((1100,1100))
    a=np.asarray(im).astype(float)/255
    mx=a.max(axis=2); mn=a.min(axis=2); sat=(mx-mn)/(mx+1e-6)
    fgm=(sat<sat_th)&(mx>v_th)
    fgm=ndi.binary_opening(fgm,iterations=3)
    fgm=ndi.binary_closing(fgm,iterations=close_it)
    lab,k=ndi.label(fgm); s=ndi.sum(fgm,lab,range(1,k+1)); fgm=lab==(1+int(np.argmax(s)))
    filled=ndi.binary_fill_holes(fgm)
    if fill_all: fgm=filled
    else:
        holes=filled&~fgm; hl,hk=ndi.label(holes); hs=ndi.sum(holes,hl,range(1,hk+1))
        fgm=fgm|np.isin(hl,[i+1 for i,v in enumerate(hs) if v<0.03*fgm.sum()])
    fgm=ndi.binary_erosion(fgm,iterations=3)
    alpha=ndi.gaussian_filter(fgm.astype(float),1.0)
    g=a.mean(axis=2)
    m=ndi.gaussian_filter(fgm.astype(float),60)+1e-6
    low=ndi.gaussian_filter(g*fgm,60)/m; target=(g*fgm).sum()/fgm.sum()
    g2=np.clip(g+0.6*(target-low),0,1); o=np.clip(g2**0.72,0,1)*255
    ys,xs=np.where(fgm)
    rgba=np.dstack([o]*3+[alpha*255]).astype(np.uint8)[max(0,ys.min()-6):ys.max()+7,max(0,xs.min()-6):xs.max()+7]
    Image.fromarray(rgba,'RGBA').save(out)
    bgp=Image.new('RGB',(rgba.shape[1],rgba.shape[0]),(215,235,245)); r=Image.fromarray(rgba,'RGBA'); bgp.paste(r,(0,0),r); bgp.save(out.replace('.png','_prev.jpg'))
    return rgba.shape
