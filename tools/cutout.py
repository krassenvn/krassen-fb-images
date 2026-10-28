"""Tach nen trang va lam trang bong anh san pham.
Dung: python3 cutout.py <anh_goc.png> <ra.png> [xoay_do]
Quy tac: nen = vung pixel min(RGB)>=250 lon hon 4000 px; co vien 5px; gamma 0.62; vet sang cheo 10%; cat sat khung; KHONG do bong."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, dst = sys.argv[1], sys.argv[2]
rot = float(sys.argv[3]) if len(sys.argv) > 3 else 0
im = Image.open(src).convert('RGB')
if rot: im = im.rotate(-rot, expand=True)
im.thumbnail((1100, 1100))
a = np.asarray(im).astype(float); mn = a.min(axis=2)
nw = mn >= 250; lab, k = ndi.label(nw); sizes = ndi.sum(nw, lab, range(1, k + 1))
bg = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 4000])
fg = ndi.binary_opening(~bg, iterations=2)
l2, k2 = ndi.label(fg); s2 = ndi.sum(fg, l2, range(1, k2 + 1)); fg = l2 == (1 + int(np.argmax(s2)))
fg = ndi.binary_erosion(fg, iterations=5)
alpha = ndi.gaussian_filter(fg.astype(float), 1.0)
g = a.mean(axis=2) / 255; out = np.clip(g ** 0.62, 0, 1) * 255
h, w = g.shape; yy, xx = np.mgrid[0:h, 0:w]
sheen = np.clip(1 - np.abs((xx / w * 0.9 + yy / h * 0.6) - 0.55) / 0.12, 0, 1) * 0.10
out = np.clip(out + 255 * sheen * fg, 0, 255)
ys, xs = np.where(fg)
rgba = np.dstack([out] * 3 + [alpha * 255]).astype(np.uint8)[max(0, ys.min() - 6):ys.max() + 7, max(0, xs.min() - 6):xs.max() + 7]
Image.fromarray(rgba, 'RGBA').save(dst)
