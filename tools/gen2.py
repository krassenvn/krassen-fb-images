import os
from playwright.sync_api import sync_playwright
CTA="Nhắn tin để được tư vấn chi tiết"
CSS="*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;font-family:'DejaVu Sans',sans-serif;position:relative}img.logo{mix-blend-mode:multiply;position:absolute}"
P=[
 dict(code='KS42TC',style=6,title='Mũi nhọn dáng chữ V<br>cao cấp, <b>rơi chậm</b>',specs=[('37×47cm','chỉnh dài 46–48cm'),('1,6kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS07',style=7,title='Rơi chậm êm ái,<br><b>nhựa PP</b> phủ bóng',specs=[('36×46cm','chỉnh dài 43–47cm'),('1,4kg','dày chắc chắn'),('Bảo hành','1 năm')]),
 dict(code='KSV42T',style=8,title='Vuông thang 33–35×45cm,<br><b>rơi chậm</b> không ồn',specs=[('33–35×45cm','chỉnh dài 45–47cm'),('1,4kg','dày chắc chắn'),('Bảo hành','1 năm')]),
 dict(code='KS23U',style=6,title='Chữ U đẹp cao cấp,<br>vừa <b>nhiều dòng bồn</b>',specs=[('36×46cm','chỉnh dài 46–48cm'),('1,5kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS22VT',style=7,title='Mũi nhọn 35×47cm,<br><b>bản lề gài</b>, rơi chậm',specs=[('35×47cm','chỉnh dài 45–48cm'),('1,4kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS23VT',style=8,title='Tròn bầu cao cấp,<br><b>ốc nhựa</b> cho bồn rời khối',specs=[('36×46cm','chỉnh dài 45–46cm'),('1,6kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS04U',style=7,title='Chữ U đúc đặc cao cấp,<br><b>dày chắc</b> 1,6kg',specs=[('36×46cm','chỉnh dài 45–46cm'),('Đúc đặc','nhựa PP cao cấp'),('Bảo hành','2 năm')]),
]
def sp(p): return ''.join(f'<div><b>{a}</b>{b}</div>' for a,b in p['specs'])
def html(p):
    img=f"img/{p['code']}_pair.png"; s=p['style']
    if s==6:  # cat nang, chu trai, vong tron lon phia sau
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(165deg,#fdf4ea,#f6dcc6);color:#4a2d1a}}
.c{{position:absolute;border-radius:50%;background:rgba(214,120,60,.10)}}
.logo{{top:34px;left:60px;width:125px}}
.code{{position:absolute;top:70px;right:70px;font-size:34px;font-weight:800;color:#c8662d;letter-spacing:3px}}
h1{{position:absolute;top:200px;left:70px;font-family:'DejaVu Serif',serif;font-size:62px;line-height:1.18;font-weight:700;width:940px}}h1 b{{color:#c8662d;font-style:italic}}
.ph{{position:absolute;left:40px;top:470px;width:1000px;height:560px;object-fit:contain}}
.sp{{position:absolute;left:70px;right:70px;top:1060px;display:flex;gap:30px}}
.sp div{{flex:1;font-size:23px;line-height:1.3;border-left:5px solid #c8662d;padding-left:16px}}.sp b{{display:block;font-size:34px;color:#c8662d}}
.cta{{position:absolute;right:70px;bottom:70px;font-size:34px;font-weight:800;color:#4a2d1a;border-bottom:5px solid #c8662d;padding-bottom:6px}}</style></head><body>
<div class=c style="width:760px;height:760px;left:160px;top:380px"></div><div class=c style="width:300px;height:300px;right:-80px;top:-60px"></div>
<img class=logo src=img/logo.jpg><div class=code>{p['code']}</div><h1>{p['title']}</h1><img class=ph src={img}><div class=sp>{sp(p)}</div><div class=cta>{CTA}</div></body></html>"""
    if s==7:  # anh truoc, tieu de duoi, nen xanh xam
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(180deg,#f3f7fb,#dbe7f2);color:#1d3557;text-align:center}}
.band{{position:absolute;left:-100px;right:-100px;top:210px;height:560px;background:rgba(70,120,180,.10);transform:skewY(-5deg)}}
.logo{{top:28px;left:455px;width:170px}}
.ph{{position:absolute;left:40px;top:190px;width:1000px;height:600px;object-fit:contain}}
.code{{position:absolute;top:815px;width:100%;font-size:34px;font-weight:800;color:#3a78b5;letter-spacing:6px}}
h1{{position:absolute;top:870px;width:100%;font-size:56px;line-height:1.2;font-weight:800}}h1 b{{color:#e8563a}}
.sp{{position:absolute;top:1070px;left:60px;right:60px;display:flex;justify-content:space-between}}
.sp div{{width:300px;font-size:23px;line-height:1.35}}.sp b{{display:block;font-size:34px;color:#1d3557}}
.cta{{position:absolute;bottom:60px;width:100%;font-size:34px;font-weight:800;color:#3a78b5}}</style></head><body>
<div class=band></div><img class=logo src=img/logo.jpg><img class=ph src={img}><div class=code>{p['code']}</div><h1>{p['title']}</h1><div class=sp>{sp(p)}</div><div class=cta>{CTA}</div></body></html>"""
    if s==8:  # thanh doc ben trai, nen xanh la nhat
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(170deg,#f6faea,#e0eec6);color:#2f4a16}}
.rail{{position:absolute;left:0;top:0;bottom:0;width:120px;background:rgba(90,140,40,.12)}}
.vcode{{position:absolute;left:34px;bottom:70px;font-size:60px;font-weight:900;color:#5a8c28;writing-mode:vertical-rl;transform:rotate(180deg);letter-spacing:6px}}
.logo{{top:34px;left:10px;width:100px}}
h1{{position:absolute;top:100px;left:170px;right:50px;font-size:56px;line-height:1.18;font-weight:800}}h1 b{{color:#5a8c28}}
.ph{{position:absolute;left:150px;top:330px;width:900px;height:640px;object-fit:contain}}
.sp{{position:absolute;left:170px;right:60px;top:1010px;display:flex;gap:26px}}
.sp div{{flex:1;font-size:23px;line-height:1.3;padding-top:10px;border-top:4px solid #5a8c28}}.sp b{{display:block;font-size:32px;color:#2f4a16}}
.cta{{position:absolute;left:170px;bottom:70px;font-size:34px;font-weight:800;color:#e2602a}}</style></head><body>
<div class=rail></div><img class=logo src=img/logo.jpg><div class=vcode>{p['code']}</div><h1>{p['title']}</h1><img class=ph src={img}><div class=sp>{sp(p)}</div><div class=cta>{CTA}</div></body></html>"""
if __name__=='__main__':
    os.makedirs('out2',exist_ok=True)
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
        for p in P:
            open(f"_n_{p['code']}.html",'w').write(html(p))
            pg.goto('file://'+os.path.abspath(f"_n_{p['code']}.html")); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out2/{p['code']}.png"); pg.screenshot(path=f"out2/{p['code']}.jpg",type='jpeg',quality=90)
        b.close()
    from PIL import Image
    ims=[Image.open(f"out2/{p['code']}.png").convert('RGB').resize((360,450)) for p in P]
    m=Image.new('RGB',(360*4,450*2),'white')
    for i,im in enumerate(ims): m.paste(im,((i%4)*360,(i//4)*450))
    m.save('out2/montage.jpg',quality=85)
