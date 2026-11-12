import os, sys
sys.path.insert(0,'.')
from PIL import Image
from compose import cut
import gen, gen3
from playwright.sync_api import sync_playwright
PAIRS={'KS09':['src/KS09N/1.png','src/KS09N/2.png'],'KS005':['src/KS005N/1.png','src/KS005N/5.png']}
for code,files in PAIRS.items():
    ims=[cut(f) for f in files]; H=620
    ims=[im.resize((max(1,int(im.width*H/im.height)),H)) for im in ims]
    gap=40; W=sum(i.width for i in ims)+gap+20
    cv=Image.new('RGBA',(W,H+20),(0,0,0,0)); x=10
    for im in ims: cv.alpha_composite(im,(x,10)); x+=im.width+gap
    cv.save(f'img/{code}_pair.png'); print(code,cv.size)
S=lambda a,b:(a,b)
OLD=[dict(code='KS09',style=5,title='Tròn bầu gọn gàng,<br><i>đóng êm</i> bền màu',specs=[S('37×44cm','chỉnh dài 43–44cm'),S('Rơi êm','đóng nhẹ, không ồn'),S('Bảo hành','2 năm')]),
     dict(code='KS005',style=1,title='Dáng trứng thanh thoát,<br>đóng <span>êm</span> rơi chậm',specs=[S('36×45cm','chỉnh dài 43–46cm'),S('1,3kg','dày chắc chắn'),S('Bảo hành','2 năm, trắng sữa phủ bóng')])]
NEW=[dict(code='KS09',style=9,title='Tròn bầu đóng êm,<br>vừa <em>nhiều dòng bồn</em>',specs=[S('37×44cm','chỉnh dài 43–44cm'),S('Rơi êm','đóng nhẹ, không ồn'),S('Bảo hành','2 năm')]),
     dict(code='KS005',style=11,title='Hình trứng nhẹ nhàng,<br>đóng <em>êm</em> rơi chậm',specs=[S('36×45cm','chỉnh dài 43–46cm'),S('1,3kg','dày chắc chắn'),S('Bảo hành','2 năm, trắng sữa phủ bóng')])]
os.makedirs('out7',exist_ok=True)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for tag,lst,mod in (('',OLD,gen),('_b',NEW,gen3)):
        for p in lst:
            fn=f"_n7_{p['code']}{tag}.html"; open(fn,'w').write(mod.html(p))
            pg.goto('file://'+os.path.abspath(fn)); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out7/{p['code']}{tag}.png"); pg.screenshot(path=f"out7/{p['code']}{tag}.jpg",type='jpeg',quality=90)
    b.close()
ims=[Image.open(f"out7/{c}{t}.png").convert('RGB').resize((540,675)) for c in ('KS09','KS005') for t in ('','_b')]
m=Image.new('RGB',(2160,675),'white')
for i,im in enumerate(ims): m.paste(im,(i*540,0))
m.save('out7/montage.jpg',quality=88); print('ok')
