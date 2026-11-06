import os, sys
sys.path.insert(0, '.')
from PIL import Image
from compose import cut
import gen2, gen3
from playwright.sync_api import sync_playwright

# --- cat nen + ghep cap ---
Image.open('src/KS5/94.png').convert('RGB').crop((22, 22, 1478, 1478)).save('src/KS5/94c.png')
PAIRS = {'KS5': ['src/KS5/94c.png', 'src/KS5/93.png'], 'KVS600': ['src/KVS600/5.png', 'src/KVS600/14.png']}
for code, files in PAIRS.items():
    ims = [cut(f) for f in files]
    H = 620; ims = [im.resize((max(1, int(im.width * H / im.height)), H)) for im in ims]
    gap = 40; W = sum(i.width for i in ims) + gap * (len(ims) - 1) + 20
    cv = Image.new('RGBA', (W, H + 20), (0, 0, 0, 0)); x = 10
    for im in ims: cv.alpha_composite(im, (x, 10)); x += im.width + gap
    cv.save(f'img/{code}_pair.png'); print(code, cv.size)

S = lambda a, b: (a, b)
OLD = [  # kieu cu (gen2 style 6/7/8)
 dict(code='KS5', style=7, title='Nắp bồn cầu 36×44cm,<br><b>bền chắc</b> cho bồn 2 khối', specs=[S('36×44cm','chỉnh dài 43–45cm'), S('1kg','bền chắc'), S('Bồn 2 khối','két nước rời')]),
 dict(code='KVS600', style=6, title='Chữ V bản đặc biệt,<br><b>dày chắc</b> 1,8kg', specs=[S('37×47cm','chỉnh dài 46–48cm'), S('1,8kg','dày chắc chắn'), S('Bảo hành','2 năm')]),
]
NEW = [  # kieu moi (gen3 style 9-12)
 dict(code='KS5', style=11, title='Cho bồn 2 khối,<br>két nước <em>rời</em>', specs=[S('36×44cm','chỉnh dài 43–45cm'), S('1kg','bền chắc'), S('Bồn 2 khối','két nước rời')]),
 dict(code='KVS600', style=12, title='Bản đặc biệt chữ V,<br>rơi chậm <em>không ồn</em>', specs=[S('37×47cm','chỉnh dài 46–48cm'), S('1,8kg','dày chắc chắn'), S('Bảo hành','2 năm')]),
]
os.makedirs('out4', exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for tag, lst, mod in (('', OLD, gen2), ('_b', NEW, gen3)):
        for p in lst:
            fn = f"_n4_{p['code']}{tag}.html"; open(fn, 'w').write(mod.html(p))
            pg.goto('file://' + os.path.abspath(fn)); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out4/{p['code']}{tag}.png")
            pg.screenshot(path=f"out4/{p['code']}{tag}.jpg", type='jpeg', quality=90)
    b.close()
ims = [Image.open(f"out4/{c}{t}.png").convert('RGB').resize((540, 675)) for c in ('KS5', 'KVS600') for t in ('', '_b')]
m = Image.new('RGB', (540 * 4, 675), 'white')
for i, im in enumerate(ims): m.paste(im, (i * 540, 0))
m.save('out4/montage.jpg', quality=88); print('xong')
