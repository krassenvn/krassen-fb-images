import os, sys, numpy as np
sys.path.insert(0, '.')
from PIL import Image
from scipy import ndimage as ndi
import gen2, gen3
from playwright.sync_api import sync_playwright

def cut_color(path):
    im = Image.open(path).convert('RGB'); im.thumbnail((1100, 1100))
    a = np.asarray(im).astype(float); mn = a.min(axis=2)
    nw = mn >= 250; lab, k = ndi.label(nw); sizes = ndi.sum(nw, lab, range(1, k + 1))
    bg = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 4000]); fg = ndi.binary_opening(~bg, iterations=2)
    l2, k2 = ndi.label(fg); s2 = ndi.sum(fg, l2, range(1, k2 + 1)); fg = l2 == (1 + int(np.argmax(s2)))
    fg = ndi.binary_fill_holes(fg)
    fg = ndi.binary_erosion(fg, iterations=4)
    alpha = ndi.gaussian_filter(fg.astype(float), 1.0)
    rgb = np.clip((a / 255) ** 0.88, 0, 1) * 255          # nang sang nhe, giu mau
    ys, xs = np.where(fg)
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)[max(0, ys.min() - 6):ys.max() + 7, max(0, xs.min() - 6):xs.max() + 7]
    return Image.fromarray(rgba, 'RGBA')

files = ['src/BX10X20CM/15.png', 'src/BX10X20CM/14.png']
ims = [cut_color(f) for f in files]
H = 620; ims = [im.resize((max(1, int(im.width * H / im.height)), H)) for im in ims]
gap = 40; W = sum(i.width for i in ims) + gap * (len(ims) - 1) + 20
cv = Image.new('RGBA', (W, H + 20), (0, 0, 0, 0)); x = 10
for im in ims: cv.alpha_composite(im, (x, 10)); x += im.width + gap
cv.save('img/BX10X20CM_pair.png'); print('pair', cv.size)

S = lambda a, b: (a, b)
OLD = dict(code='BX10X20CM', style=8, title='Bộ xả cao cấp 10×20cm,<br><b>nhựa ABS</b> phủ bóng', specs=[S('10×20cm','cổ xả 10cm, cao 20cm'), S('Nhựa ABS','cao cấp phủ bóng'), S('Bảo hành','3 năm')])
NEW = dict(code='BX10X20CM', style=10, title='Cho bồn cầu liền khối,<br>cổ xả 10cm – cao <em>20cm</em>', specs=[S('10×20cm','cổ xả 10cm, cao 20cm'), S('Nhựa ABS','cao cấp phủ bóng'), S('Bảo hành','3 năm')])
os.makedirs('out5', exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for tag, p, mod in (('', OLD, gen2), ('_b', NEW, gen3)):
        fn = f"_n5_{p['code']}{tag}.html"; open(fn, 'w').write(mod.html(p))
        pg.goto('file://' + os.path.abspath(fn)); pg.wait_for_timeout(250)
        pg.screenshot(path=f"out5/{p['code']}{tag}.png"); pg.screenshot(path=f"out5/{p['code']}{tag}.jpg", type='jpeg', quality=90)
    b.close()
ims = [Image.open(f"out5/BX10X20CM{t}.png").convert('RGB').resize((540, 675)) for t in ('', '_b')]
m = Image.new('RGB', (1080, 675), 'white')
for i, im in enumerate(ims): m.paste(im, (i * 540, 0))
m.save('out5/montage.jpg', quality=88); print('xong')
