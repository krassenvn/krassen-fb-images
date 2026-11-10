"""Chuẩn hóa ảnh sản phẩm: nền trắng, cân trắng đồng đều, logo Krassen chìm ở giữa. 1080x1080 JPG."""
import sys, numpy as np
from PIL import Image
S=1080; FIT=900; WM_W=520; WM_OP=0.10
def logo_rgba(path):
    lg=Image.open(path).convert('RGB'); a=np.asarray(lg).astype(float)
    dist=255-a.min(axis=2)            # độ đậm so với trắng
    alpha=np.clip(dist*2.2,0,255)
    out=np.dstack([a,alpha]).astype(np.uint8)
    return Image.fromarray(out,'RGBA')
def process(src,dst,logo):
    im=Image.open(src).convert('RGBA')
    bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg
    a=np.asarray(im).astype(float); rgb=a[...,:3]
    m=rgb.min(axis=2)<248                 # vùng sản phẩm (khác nền trắng)
    ys,xs=np.where(m); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    a=a[y0:y1,x0:x1]; rgb=a[...,:3]; m=m[y0:y1,x0:x1]
    lum=rgb.mean(axis=2); sat=rgb.max(axis=2)-rgb.min(axis=2)
    sel=m&(lum>=np.percentile(lum[m],60))&(sat<40)
    mean=rgb[sel].mean(axis=0)
    gain=mean.mean()/mean                 # khử ám màu (xanh/vàng/xám)
    rgb=rgb*gain
    l2=rgb.mean(axis=2); p=np.percentile(l2[m],92)
    rgb=rgb*(246/p)                       # đưa vùng trắng về cùng độ sáng
    rgb=255*np.power(np.clip(rgb,0,255)/255,0.95)
    rgb[~m]=255                           # nền trắng tuyệt đối
    out=np.dstack([np.clip(rgb,0,255),np.full(m.shape,255.)]).astype(np.uint8)
    pr=Image.fromarray(out,'RGBA'); pr.thumbnail((FIT,FIT),Image.LANCZOS)
    can=Image.new('RGBA',(S,S),(255,255,255,255))
    can.alpha_composite(pr,((S-pr.width)//2,(S-pr.height)//2))
    wm=logo.copy(); wm.thumbnail((WM_W,WM_W),Image.LANCZOS)
    wa=np.asarray(wm).astype(float); wa[...,3]*=WM_OP; wm=Image.fromarray(wa.astype(np.uint8),'RGBA')
    can.alpha_composite(wm,((S-wm.width)//2,(S-wm.height)//2))
    can.convert('RGB').save(dst,'JPEG',quality=88,optimize=True)
    print(dst,'gain',np.round(gain,3))
if __name__=='__main__':
    logo=logo_rgba(sys.argv[1]); outdir=sys.argv[2]
    for i,s in enumerate(sys.argv[3:],1): process(s,f'{outdir}/{i:02d}.jpg',logo)
