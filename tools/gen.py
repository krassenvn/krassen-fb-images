import os, json
from playwright.sync_api import sync_playwright

CTA="Nhắn tin để được tư vấn chi tiết"
P=[  # code, img, style, title (html), specs [(big,small)x3], tag
 dict(code='KS500RK',img='rk_open',style=1,title='Nắp bồn cầu <span>rơi êm</span><br>mũi nhọn – đáy bo',specs=[('37×47cm','chỉnh dài 47–48cm'),('Nhựa PP','nguyên sinh, bóng, chống trầy'),('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS11',img='ks11',style=2,title='Tròn bầu <i>đóng êm</i>,<br>vừa vặn mọi nhà',specs=[('36×44cm','chỉnh dài 43–44cm'),('Rơi êm','đóng nhẹ, không ồn'),('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS609TC',img='tc609',style=3,title='Mũi nhọn chữ <span>V</span><br>đáy rộng · rơi chậm',specs=[('36×46cm','chỉnh 45–47cm'),('Rơi chậm','không gây tiếng ồn'),('Bảo hành','2 năm')]),
 dict(code='KS500LK',img='lk500',style=4,title='Mũi nhọn thanh lịch,<br><span>rơi êm</span> đáy bo',specs=[('37×47cm','chỉnh dài 47–48cm'),('Nhựa PP','nguyên sinh, bóng, chống trầy'),('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS09',img='ks09',style=5,title='Tròn bầu gọn gàng,<br><i>đóng êm</i> bền màu',specs=[('37×44cm','chỉnh dài 43–44cm'),('Rơi êm','đóng nhẹ, không ồn'),('Bảo hành','2 năm')]),
 dict(code='KS15U',img='ks15u',style=2,title='Nắp chữ U <i>rơi chậm</i>,<br>êm ái không tiếng ồn',specs=[('36×46cm','chỉnh dài 45–48cm'),('1,4kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS005',img='ks005',style=1,title='Dáng trứng thanh thoát,<br>đóng <span>êm</span> rơi chậm',specs=[('36×45cm','chỉnh dài 43–46cm'),('1,3kg','dày chắc chắn'),('Bảo hành','2 năm, trắng sữa phủ bóng')]),
 dict(code='KS21',img='ks21',style=3,title='Dáng nhỏ gọn mũi tròn,<br>rơi chậm <span>êm ái</span>',specs=[('34×44cm','chỉnh dài 43–44cm'),('1,3kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS504C',img='ks504c',style=4,title='Mũi tròn đáy rộng,<br><span>rơi chậm</span> bền màu',specs=[('36×46cm','chỉnh dài 44–47cm'),('Nhựa PP','cao cấp không ố màu'),('Bảo hành','2 năm')]),
 dict(code='KS45',img='ks45',style=5,title='Nắp cao cấp rơi êm,<br><i>gắn vòi xịt</i> tiện lợi',specs=[('37×47cm','chỉnh dài 47–48cm'),('1,7kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS602K',img='ks602k',style=2,title='Mũi nhọn đáy bo,<br><i>rơi chậm</i> không ồn',specs=[('36×47cm','chỉnh dài 46–48cm'),('1,5kg','dày chắc chắn'),('Bảo hành','2 năm')]),
 dict(code='KS608U',img='ks608u',style=1,title='Chữ U cỡ nhỏ gọn,<br>sang trọng <span>bền màu</span>',specs=[('34×44cm','chỉnh dài 43–44cm'),('Nhựa PP','trắng sữa phủ bóng'),('Bảo hành','2 năm')]),

 dict(code='KSV43',img='ksv43',style=3,title='Nắp vuông mũi nhô,<br>rơi chậm <span>êm ái</span>',specs=[('35×43cm','chỉnh dài 43–45cm'),('1,3kg','dày chắc chắn'),('Bảo hành','12 tháng')]),
]
def spec3(p,cls):
    return ''.join(f'<div><b>{a}</b>{b}</div>' for a,b in p['specs'])
CSS="*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;font-family:'DejaVu Sans',sans-serif;position:relative}img.logo{mix-blend-mode:multiply;position:absolute}"
def html(p):
    s=p['style']; img=f"img/{p['code']}_pair.png"; sp=spec3(p,'')
    if s==1:
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(170deg,#f2fafd,#d7eef7);color:#0b3c5d}}
.c{{position:absolute;border-radius:50%;background:rgba(20,150,168,.10)}}
.logo{{top:28px;left:60px;width:125px}}
.code{{position:absolute;top:56px;right:70px;background:#0b3c5d;color:#fff;font-weight:800;font-size:30px;padding:10px 26px;border-radius:40px}}
h1{{position:absolute;top:190px;left:70px;width:940px;font-size:64px;line-height:1.15;font-weight:800}}h1 span{{color:#e8463a}}
.ph{{position:absolute;left:50px;top:440px;width:900px;height:580px;object-fit:contain}}
.badge{{position:absolute;top:292px;right:32px;width:190px;height:190px;border-radius:50%;background:#e8463a;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(8deg);text-align:center;font-size:20px;line-height:1.3}}.badge b{{font-size:27px}}
.sp{{position:absolute;bottom:60px;left:70px;right:70px;display:flex;gap:18px}}
.sp div{{flex:1;padding:14px 12px;text-align:center;font-size:23px;line-height:1.3;border-top:3px solid #1496a8}}.sp b{{display:block;font-size:34px;color:#e8463a;margin-bottom:4px}}
.cta{{position:absolute;bottom:235px;left:70px;font-size:30px;color:#2d6a85}}</style></head><body>
<div class=c style="width:600px;height:600px;top:-200px;right:-200px"></div><div class=c style="width:420px;height:420px;bottom:-120px;left:-140px"></div>
<img class=logo src=img/logo.jpg><div class=code>{p['code']}</div><h1>{p['title']}</h1><img class=ph src={img}>
<div class=badge>Nhắn tin để<br>được tư vấn<br><b>chi tiết</b></div>
<div class=cta>Krassen · Nắp bồn cầu chính hãng</div><div class=sp>{sp}</div></body></html>"""
    if s==2:
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:#fbf3e6;color:#3b2a20}}
.blob{{position:absolute;right:-220px;bottom:-200px;width:700px;height:700px;border-radius:50%;background:#f7d3c3}}
.logo{{top:36px;right:60px;width:130px}}
.tag{{position:absolute;top:70px;left:90px;font-size:26px;letter-spacing:6px;color:#b5543c;font-weight:700}}
h1{{position:absolute;top:120px;left:90px;width:900px;font-family:'DejaVu Serif',serif;font-size:66px;line-height:1.14}}h1 i{{color:#b5543c}}
.ph{{position:absolute;left:40px;top:330px;width:1000px;height:520px;object-fit:contain}}
.sp{{position:absolute;left:90px;right:90px;top:880px;display:flex;gap:24px}}
.sp div{{flex:1;padding:8px 0 8px 16px;border-left:5px solid #b5543c;font-size:22px;line-height:1.3}}.sp b{{display:block;font-size:32px;color:#b5543c}}
.code{{position:absolute;left:90px;top:1010px;color:#b5543c;font-weight:800;font-size:44px;letter-spacing:2px}}
.bar{{position:absolute;left:90px;bottom:70px;right:90px;height:110px;border-radius:55px;background:#3b2a20;color:#fbf3e6;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:700}}</style></head><body>
<div class=blob></div><img class=logo src=img/logo.jpg><div class=tag>KRASSEN · NẮP BỒN CẦU</div><h1>{p['title']}</h1>
<img class=ph src={img}><div class=code>{p['code']}</div><div class=sp>{sp}</div><div class=bar>{CTA}</div></body></html>"""
    if s==3:
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:radial-gradient(circle at 50% 40%,#fffdf7,#f4e8c8);color:#3a2f14;text-align:center}}
.logo{{top:30px;left:455px;width:170px}}
h1{{position:absolute;top:200px;width:100%;font-family:'DejaVu Serif',serif;font-size:62px;line-height:1.2}}h1 span{{color:#a8802c}}
.line{{position:absolute;top:432px;left:440px;width:200px;height:3px;background:#a8802c}}
.ph{{position:absolute;left:40px;top:470px;width:1000px;height:590px;object-fit:contain}}
.code{{position:absolute;top:385px;width:100%;color:#a8802c;font-weight:800;font-size:34px;letter-spacing:4px}}
.sp{{position:absolute;top:1105px;width:100%;display:flex;justify-content:center;gap:60px;font-size:25px;color:#5a4a22}}.sp b{{display:block;font-size:34px;color:#a8802c;margin-bottom:4px}}
.bot{{position:absolute;bottom:70px;width:100%;font-size:34px;letter-spacing:2px;color:#3a2f14;font-weight:700}}</style></head><body>
<img class=logo src=img/logo.jpg><h1>{p['title']}</h1><div class=line></div><img class=ph src={img}><div class=code>{p['code']}</div>
<div class=sp>{sp}</div><div class=bot>{CTA}</div></body></html>"""
    if s==4:
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(180deg,#f0faf5,#d6f0e3);color:#12453a}}
.ghost{{position:absolute;top:340px;left:-10px;font-size:280px;font-weight:900;color:rgba(18,69,58,.06);letter-spacing:-8px;white-space:nowrap}}
.logo{{top:30px;right:60px;width:125px}}
.tag{{position:absolute;top:62px;left:70px;font-size:26px;letter-spacing:7px;color:#1f9d75;font-weight:700}}
h1{{position:absolute;top:130px;left:70px;width:900px;font-size:60px;line-height:1.15;font-weight:800}}h1 span{{color:#1f9d75}}
.ph{{position:absolute;left:40px;top:350px;width:1000px;height:650px;object-fit:contain}}
.code{{position:absolute;left:70px;top:1030px;font-size:46px;font-weight:800;color:#1f9d75;letter-spacing:2px}}
.ask{{position:absolute;right:70px;top:1025px;text-align:right;font-size:30px;font-weight:700;color:#e0572f;line-height:1.25}}
.sp{{position:absolute;left:70px;right:70px;bottom:60px;display:flex;justify-content:space-between;border-top:3px solid #1f9d75;padding-top:20px}}
.sp div{{font-size:23px;line-height:1.35;width:300px}}.sp b{{display:block;font-size:32px;color:#12453a}}</style></head><body>
<div class=ghost>{p['code']}</div><img class=logo src=img/logo.jpg><div class=tag>KRASSEN · NẮP BỒN CẦU</div><h1>{p['title']}</h1>
<img class=ph src={img}><div class=code>{p['code']}</div><div class=ask>Nhắn tin để được<br>tư vấn chi tiết</div><div class=sp>{sp}</div></body></html>"""
    if s==5:
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(160deg,#faf5fb,#e6dff3);color:#3a2f5c;text-align:center}}
.logo{{top:30px;left:70px;width:125px}}
.code{{position:absolute;top:60px;right:70px;font-size:36px;font-weight:800;color:#7a5cc7;letter-spacing:2px}}
h1{{position:absolute;top:190px;width:100%;font-family:'DejaVu Serif',serif;font-size:60px;line-height:1.2}}h1 i{{color:#7a5cc7}}
.ph{{position:absolute;left:40px;top:400px;width:1000px;height:560px;object-fit:contain}}
.ask{{position:absolute;top:985px;width:100%;font-size:40px;font-weight:800;color:#7a5cc7}}
.sep{{position:absolute;bottom:170px;left:70px;right:70px;height:3px;background:#7a5cc7;opacity:.5}}
.sp{{position:absolute;bottom:60px;left:70px;right:70px;display:flex;justify-content:space-between}}
.sp div{{width:300px;font-size:23px;line-height:1.35}}.sp b{{display:block;font-size:32px;color:#3a2f5c}}</style></head><body>
<img class=logo src=img/logo.jpg><div class=code>{p['code']}</div><h1>{p['title']}</h1><img class=ph src={img}>
<div class=ask>{CTA}</div><div class=sep></div><div class=sp>{sp}</div></body></html>"""
if __name__=='__main__':
    os.makedirs('out',exist_ok=True)
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
        for i,p in enumerate(P):
            open(f"_{p['code']}.html",'w').write(html(p))
            pg.goto('file://'+os.path.abspath(f"_{p['code']}.html")); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out/{p['code']}.png")
            pg.screenshot(path=f"out/{p['code']}.jpg",type='jpeg',quality=90)
        b.close()
    # montage
    from PIL import Image
    ims=[Image.open(f"out/{p['code']}.png").convert('RGB').resize((360,450)) for p in P]
    m=Image.new('RGB',(360*4,450*3),'white')
    for i,im in enumerate(ims): m.paste(im,((i%4)*360,(i//4)*450))
    m.save('out/montage.jpg',quality=85)
