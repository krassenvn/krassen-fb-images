import numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.spatial import ConvexHull
def gc(path,rot,out,hull=False):
    im=Image.open(path).convert('RGB')
    if rot: im=im.rotate(rot,expand=True)
    im.thumbnail((900,900)); a=np.asarray(im)
    f=a.astype(float)/255; mx=f.max(2); mn=f.min(2); sat=(mx-mn)/(mx+1e-6)
    base=(sat<0.16)&(mx>0.58); base=ndi.binary_opening(base,iterations=3); base=ndi.binary_closing(base,iterations=8)
    lab,k=ndi.label(base); s=ndi.sum(base,lab,range(1,k+1)); base=lab==(1+int(np.argmax(s)))
    sure_fg=ndi.binary_erosion(base,iterations=18); prob_fg=ndi.binary_dilation(base,iterations=12)
    mask=np.full(base.shape,cv2.GC_BGD,np.uint8); mask[prob_fg]=cv2.GC_PR_BGD; mask[base]=cv2.GC_PR_FGD; mask[sure_fg]=cv2.GC_FGD
    bg=np.zeros((1,65)); fg=np.zeros((1,65))
    cv2.grabCut(cv2.cvtColor(a,cv2.COLOR_RGB2BGR),mask,None,bg,fg,8,cv2.GC_INIT_WITH_MASK)
    m=(mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD); m=ndi.binary_opening(m,iterations=2)
    lab,k=ndi.label(m); s=ndi.sum(m,lab,range(1,k+1)); m=lab==(1+int(np.argmax(s)))
    if hull:
        ys,xs=np.where(m); pts=np.c_[xs,ys][::5]; h=ConvexHull(pts)
        im2=Image.new('L',(m.shape[1],m.shape[0]),0); ImageDraw.Draw(im2).polygon([tuple(pts[i]) for i in h.vertices],fill=1); m=np.asarray(im2).astype(bool)
    m=ndi.gaussian_filter(m.astype(float),3)>0.5; m=ndi.binary_erosion(m,iterations=2)
    alpha=ndi.gaussian_filter(m.astype(float),1.0)
    g=a.mean(2)/255; mm=ndi.gaussian_filter(m.astype(float),60)+1e-6
    low=ndi.gaussian_filter(g*m,60)/mm; t=(g*m).sum()/m.sum()
    g2=np.clip(g+0.6*(t-low),0,1); o=np.clip(g2**0.72,0,1)*255
    ys,xs=np.where(m)
    rgba=np.dstack([o]*3+[alpha*255]).astype(np.uint8)[max(0,ys.min()-6):ys.max()+7,max(0,xs.min()-6):xs.max()+7]
    Image.fromarray(rgba,'RGBA').save(out); return rgba.shape
