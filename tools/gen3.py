import os, sys
from playwright.sync_api import sync_playwright
CTA = "Nhắn tin để được tư vấn chi tiết"
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;font-family:'DejaVu Sans',sans-serif;position:relative}img.logo{mix-blend-mode:multiply;position:absolute}em{font-style:normal}"

# 20 ma: style 9 hong, 10 vang bo, 11 xanh ngoc, 12 xam-san ho. Thong so lay tu ban cu / Sheet.
def S(a, b): return (a, b)
P = [
 dict(code='KS500RK', style=9,  title='Mũi nhọn đáy bo,<br>rơi <em>êm</em> từng lần đóng', specs=[S('37×47cm','chỉnh dài 47–48cm'),S('Nhựa PP','nguyên sinh, bóng, chống trầy'),S('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS11',    style=10, title='Cho bồn cầu dáng tròn bầu:<br><em>đóng êm</em> vừa vặn', specs=[S('36×44cm','chỉnh dài 43–44cm'),S('Rơi êm','đóng nhẹ, không ồn'),S('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS609TC', style=11, title='Chữ V sắc nét,<br>rơi chậm <em>không ồn</em>', specs=[S('36×46cm','chỉnh 45–47cm'),S('Rơi chậm','không gây tiếng ồn'),S('Bảo hành','2 năm')]),
 dict(code='KS500LK', style=12, title='Thanh lịch mũi nhọn,<br>gọn gàng <em>đáy bo</em>', specs=[S('37×47cm','chỉnh dài 47–48cm'),S('Nhựa PP','nguyên sinh, bóng, chống trầy'),S('Bảo hành','2 năm đóng êm &amp; độ bền màu')]),
 dict(code='KS09',    style=9,  title='Tròn bầu đóng êm,<br>vừa <em>nhiều dòng bồn</em>', specs=[S('37×44cm','chỉnh dài 43–44cm'),S('Rơi êm','đóng nhẹ, không ồn'),S('Bảo hành','2 năm')]),
 dict(code='KS15U',   style=10, title='Chữ U êm ái,<br>rơi chậm <em>không tiếng ồn</em>', specs=[S('36×46cm','chỉnh dài 45–48cm'),S('1,4kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS005',   style=11, title='Hình trứng nhẹ nhàng,<br>đóng <em>êm</em> rơi chậm', specs=[S('36×45cm','chỉnh dài 43–46cm'),S('1,3kg','dày chắc chắn'),S('Bảo hành','2 năm, trắng sữa phủ bóng')]),
 dict(code='KS21',    style=12, title='Phòng tắm nhỏ?<br>Chọn nắp <em>nhỏ gọn</em>', specs=[S('34×44cm','chỉnh dài 43–44cm'),S('1,3kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS504C',  style=9,  title='Mũi tròn đáy rộng,<br>trắng sữa <em>không ố màu</em>', specs=[S('36×46cm','chỉnh dài 44–47cm'),S('Nhựa PP','cao cấp không ố màu'),S('Bảo hành','2 năm')]),
 dict(code='KS45',    style=10, title='Gắn vòi xịt tiện lợi,<br>dày chắc <em>1,7kg</em>', specs=[S('37×47cm','chỉnh dài 47–48cm'),S('1,7kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS602K',  style=11, title='Dày chắc 1,5kg,<br>rơi chậm <em>không ồn</em>', specs=[S('36×47cm','chỉnh dài 46–48cm'),S('1,5kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS608U',  style=12, title='Chữ U gọn gàng,<br>trắng sữa <em>phủ bóng</em>', specs=[S('34×44cm','chỉnh dài 43–44cm'),S('Nhựa PP','trắng sữa phủ bóng'),S('Bảo hành','2 năm')]),
 dict(code='KSV43',   style=9,  title='Dành cho bồn vuông,<br>kích thước <em>35×43cm</em>', specs=[S('35×43cm','chỉnh dài 43–45cm'),S('1,3kg','dày chắc chắn'),S('Bảo hành','12 tháng')]),
 dict(code='KS42TC',  style=10, title='Dáng chữ V mũi nhọn,<br>dày chắc <em>1,6kg</em>', specs=[S('37×47cm','chỉnh dài 46–48cm'),S('1,6kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS07',    style=11, title='Rơi chậm êm ái,<br>nhựa PP <em>trắng sữa</em>', specs=[S('36×46cm','chỉnh dài 43–47cm'),S('1,4kg','dày chắc chắn'),S('Bảo hành','1 năm')]),
 dict(code='KSV42T',  style=12, title='Thay cho bồn V42<br>và <em>dáng vuông</em> tương tự', specs=[S('33–35×45cm','chỉnh dài 45–47cm'),S('1,4kg','dày chắc chắn'),S('Bảo hành','1 năm')]),
 dict(code='KS23U',   style=9,  title='Chữ U cao cấp 36×46cm,<br>rơi chậm <em>không ồn</em>', specs=[S('36×46cm','chỉnh dài 46–48cm'),S('1,5kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS22VT',  style=10, title='Mũi nhọn 35×47cm,<br>kiểu <em>bản lề gài</em>', specs=[S('35×47cm','chỉnh dài 45–48cm'),S('1,4kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS23VT',  style=11, title='Cho bồn rời khối:<br>kèm <em>ốc nhựa</em>', specs=[S('36×46cm','chỉnh dài 45–46cm'),S('1,6kg','dày chắc chắn'),S('Bảo hành','2 năm')]),
 dict(code='KS04U',   style=12, title='U đúc đặc 1,6kg,<br>đóng <em>nhẹ nhàng</em>', specs=[S('36×46cm','chỉnh dài 45–46cm'),S('Đúc đặc','nhựa PP cao cấp'),S('Bảo hành','2 năm')]),
]

def chips(p):   # 3 o ngang
    return ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in p['specs'])
def rows(p):    # 3 dong
    return ''.join(f'<div class=r><b>{a}</b><span>{b}</span></div>' for a, b in p['specs'])

def html(p):
    s = p['style']; img = f"img/{p['code']}_pair.png"; code = p['code']
    if s == 9:   # hong phan, vong tron mem, 3 o bo goc
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(170deg,#fff7f8,#fbe0e6);color:#5a1f2b}}
.c{{position:absolute;border-radius:50%;background:rgba(214,69,93,.09)}}
.logo{{top:30px;left:60px;width:125px}}
.code{{position:absolute;top:52px;right:60px;background:#d6455d;color:#fff;font-weight:800;font-size:30px;padding:10px 28px;border-radius:40px;letter-spacing:2px}}
h1{{position:absolute;top:190px;left:70px;width:940px;font-size:62px;line-height:1.17;font-weight:800}}h1 em{{color:#d6455d}}
.ph{{position:absolute;left:40px;top:455px;width:1000px;height:560px;object-fit:contain}}
.sp{{position:absolute;top:1055px;left:60px;right:60px;display:flex;gap:16px}}
.sp div{{flex:1;background:rgba(214,69,93,.10);border-radius:26px;padding:16px 12px;text-align:center;font-size:22px;line-height:1.3}}.sp b{{display:block;font-size:31px;color:#d6455d;margin-bottom:3px}}
.cta{{position:absolute;bottom:50px;width:100%;text-align:center;font-size:34px;font-weight:800;color:#d6455d}}</style></head><body>
<div class=c style="width:780px;height:780px;left:150px;top:380px"></div><div class=c style="width:320px;height:320px;right:-90px;top:-70px"></div>
<img class=logo src=img/logo.jpg><div class=code>{code}</div><h1>{p['title']}</h1><img class=ph src={img}><div class=sp>{chips(p)}</div><div class=cta>{CTA}</div></body></html>"""
    if s == 10:  # vang bo, can giua, danh sach 3 dong co dau tich
        rws = ''.join(f'<div class=r><i>✔</i><b>{a}</b> – {b}</div>' for a, b in p['specs'])
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(180deg,#fffcea,#fbefb8);color:#4a3b00;text-align:center}}
.sun{{position:absolute;left:190px;top:330px;width:700px;height:700px;border-radius:50%;background:rgba(240,190,40,.16)}}
.logo{{top:26px;left:455px;width:170px}}
.code{{position:absolute;top:190px;width:100%;font-size:30px;font-weight:800;color:#c68a00;letter-spacing:8px}}
h1{{position:absolute;top:245px;width:100%;font-size:58px;line-height:1.18;font-weight:800}}h1 em{{color:#c68a00}}
.ph{{position:absolute;left:40px;top:490px;width:1000px;height:540px;object-fit:contain}}
.rs{{position:absolute;top:1060px;left:110px;right:80px;text-align:left}}
.r{{font-size:27px;line-height:1.3;margin-bottom:12px;color:#5a4a10}}.r i{{font-style:normal;color:#c68a00;margin-right:12px;font-weight:800}}.r b{{color:#4a3b00;font-size:29px}}
.cta{{position:absolute;bottom:42px;width:100%;font-size:33px;font-weight:800;color:#4a3b00}}</style></head><body>
<div class=sun></div><img class=logo src=img/logo.jpg><div class=code>{code}</div><h1>{p['title']}</h1><img class=ph src={img}><div class=rs>{rws}</div><div class=cta>{CTA}</div></body></html>"""
    if s == 11:  # xanh ngoc, san pham tren, nem cheo duoi
        return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(180deg,#f2fcfc,#d3f0f1);color:#0b3b40}}
.wedge{{position:absolute;left:0;right:0;top:800px;bottom:0;background:rgba(14,143,150,.12);clip-path:polygon(0 14%,100% 0,100% 100%,0 100%)}}
.logo{{top:28px;left:60px;width:125px}}
.code{{position:absolute;top:52px;right:70px;font-size:42px;font-weight:800;color:#0e8f96;letter-spacing:3px;border-bottom:5px solid #0e8f96;padding-bottom:4px}}
.ph{{position:absolute;left:40px;top:170px;width:1000px;height:620px;object-fit:contain}}
h1{{position:absolute;top:850px;left:70px;width:940px;font-size:56px;line-height:1.18;font-weight:800}}h1 em{{color:#0e8f96}}
.sp{{position:absolute;top:1060px;left:70px;right:70px;display:flex}}
.sp div{{flex:1;padding:6px 14px;font-size:22px;line-height:1.3;border-left:3px solid #0e8f96}}.sp b{{display:block;font-size:31px;color:#0b3b40;margin-bottom:3px}}
.cta{{position:absolute;bottom:50px;left:70px;font-size:34px;font-weight:800;color:#0e8f96}}</style></head><body>
<div class=wedge></div><img class=logo src=img/logo.jpg><div class=code>{code}</div><img class=ph src={img}><h1>{p['title']}</h1><div class=sp>{chips(p)}</div><div class=cta>{CTA} →</div></body></html>"""
    # 12: toi gian xam sang + san ho, bang thong so
    return f"""<html><head><meta charset=utf-8><style>{CSS}
body{{background:linear-gradient(180deg,#fcfbf9,#eeeae4);color:#2b2d42}}
.ghost{{position:absolute;top:36px;left:40px;font-size:180px;font-weight:900;letter-spacing:-5px;color:transparent;-webkit-text-stroke:3px rgba(43,45,66,.10);white-space:nowrap}}
.logo{{top:30px;right:60px;width:125px}}
h1{{position:absolute;top:210px;left:70px;width:940px;font-size:62px;line-height:1.16;font-weight:800}}h1 em{{color:#ee6c4d}}
.ph{{position:absolute;left:40px;top:470px;width:1000px;height:540px;object-fit:contain}}
.tb{{position:absolute;top:1030px;left:70px;right:70px}}
.r{{display:flex;justify-content:space-between;align-items:baseline;padding:10px 0;border-bottom:2px solid rgba(43,45,66,.15);font-size:24px;color:#555a78}}.r b{{font-size:30px;color:#2b2d42}}
.cta{{position:absolute;bottom:42px;left:70px;right:70px;height:78px;border-radius:40px;background:#ee6c4d;color:#fff;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:800}}</style></head><body>
<div class=ghost>{code}</div><img class=logo src=img/logo.jpg><h1>{p['title']}</h1><img class=ph src={img}><div class=tb>{rows(p)}</div><div class=cta>{CTA}</div></body></html>"""

if __name__ == '__main__':
    only = sys.argv[1:]  # tuy chon: danh sach ma
    os.makedirs('out3', exist_ok=True)
    todo = [p for p in P if not only or p['code'] in only]
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        for p in todo:
            fn = f"_b_{p['code']}.html"; open(fn, 'w').write(html(p))
            pg.goto('file://' + os.path.abspath(fn)); pg.wait_for_timeout(250)
            pg.screenshot(path=f"out3/{p['code']}.png")
            pg.screenshot(path=f"out3/{p['code']}.jpg", type='jpeg', quality=90)
        b.close()
    from PIL import Image
    ims = [Image.open(f"out3/{p['code']}.png").convert('RGB').resize((360, 450)) for p in todo]
    cols = 5; rows_ = (len(ims) + cols - 1) // cols
    m = Image.new('RGB', (360 * cols, 450 * rows_), 'white')
    for i, im in enumerate(ims): m.paste(im, ((i % cols) * 360, (i // cols) * 450))
    m.save('out3/montage.jpg', quality=85)
    print('xong', len(todo))
