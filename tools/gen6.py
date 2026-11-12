import os, sys, shutil
sys.path.insert(0, '.')
from PIL import Image
from compose import cut
import gen2, gen3
from playwright.sync_api import sync_playwright

shutil.copy('img/KS04U_pair.png', 'img/KS07U_pair.png')
shutil.copy('img/KVS600_pair.png', 'img/KSV600_pair.png')
PAIRS = {'KS09U': ['src/KS09U/1.png', 'src/KS09U/2.png'], 'KS12VB': ['src/KS12VB/2.png', 'src/KS12VB/15.png']}
for code, files in PAIRS.items():
    ims = [cut(f) for f in files]
    H = 620; ims = [im.resize((max(1, int(im.width * H / im.height)), H)) for im in ims]
    gap = 40; W = sum(i.width for i in ims) + gap * (len(ims) - 1) + 20
    cv = Image.new('RGBA', (W, H + 20), (0, 0, 0, 0)); x = 10
    for im in ims: cv.alpha_composite(im, (x, 10)); x += im.width + gap
    cv.save(f'img/{code}_pair.png'); print(code, cv.size)

S = lambda a, b: (a, b)
OLD = [
 dict(code='KS07U', style=7, title='Chữ U đúc đặc cao cấp,<br><b>dày chắc</b> 1,6kg', specs=[S('36×46cm','chỉnh dài 45–46cm'), S('Đúc đặc','nhựa PP cao cấp'), S('Bảo hành','2 năm')]),
 dict(code='KSV600', style=6, title='Chữ V bản đặc biệt,<br><b>dày chắc</b> 1,8kg', specs=[S('37×47cm','chỉnh dài 46–48cm'), S('1,8kg','dày chắc chắn'), S('Bảo hành','2 năm')]),
 dict(code='KS09U', style=8, title='Chữ U chụp kín bệ ngồi,<br><b>rơi chậm</b> không ồn', specs=[S('36×46cm','chỉnh dài 46–48cm'), S('1,4kg','dày chắc chắn'), S('Bảo hành','1 năm')]),
 dict(code='KS12VB', style=6, title='Vuông bo 34×45cm,<br><b>rơi chậm</b> không ồn', specs=[S('34×45cm','chỉnh dài 45–46cm'), S('1,2kg','nhựa PP cao cấp'), S('Bảo hành','1 năm')]),
]
NEW = [
 dict(code='KS07U', style=12, title='U đúc đặc 1,6kg,<br>đóng <em>nhẹ nhàng</em>', specs=[S('36×46cm','chỉnh dài 45–46cm'), S('Đúc đặc','nhựa PP cao cấp'), S('Bảo hành','2 năm')]),
 dict(code='KSV600', style=12, title='Bản đặc biệt chữ V,<br>rơi chậm <em>không ồn</em>', specs=[S('37×47cm','chỉnh dài 46–48cm'), S('1,8kg','dày chắc chắn'), S('Bảo hành','2 năm')]),
 dict(code='KS09U', style=9, title='Chụp kín bệ ngồi,<br>hạn chế <em>nước ướt</em>', specs=[S('36×46cm','chỉnh dài 46–48cm'), S('1,4kg','dày chắc chắn'), S('Bảo hành','1 năm')]),
 dict(code='KS12VB', style=10, title='Vuông bo hiện đại,<br>rơi chậm <em>không ồn</em>', specs=[S('34×45cm','chỉnh dài 45–46cm'), S('1,2kg','nhựa PP cao cấp'), S('Bảo hành','1 năm')]),
]
os.makedirs('out6', exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
    for tag, lst, mod in (('', OLD, gen2), ('_b', NEW, gen3)):
        for p in lst:
            fn = f"_n6_{p['code']}{tag}.html"; open(fn, 'w').write(mod.html(p))
            pg.goto('file://' + os.path.abspath(fn)); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out6/{p['code']}{tag}.png")
            pg.screenshot(path=f"out6/{p['code']}{tag}.jpg", type='jpeg', quality=90)
    b.close()
def mont(codes, name):
    ims = [Image.open(f"out6/{c}{t}.png").convert('RGB').resize((540, 675)) for c in codes for t in ('', '_b')]
    m = Image.new('RGB', (540 * 4, 675), 'white')
    for i, im in enumerate(ims): m.paste(im, (i * 540, 0))
    m.save(name, quality=88)
mont(['KS09U', 'KS12VB'], 'out6/montage_new.jpg'); mont(['KS07U', 'KSV600'], 'out6/montage_rename.jpg'); print('xong')
