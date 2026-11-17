"""Chuẩn hóa ảnh sản phẩm cho bài 6 ảnh: nền trắng, sản phẩm trắng sáng đồng đều,
bóng mờ nhẹ như đặt trên mặt bàn, logo Krassen chìm nhỏ ở giữa. Xuất 1080x1080 JPG.
Dùng: python3 make6.py logo.jpg <thư mục ra> <ảnh 1> ... <ảnh 6>"""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

S = 1080; FIT = 860; WM_W = 130; WM_OP = 0.10; WHITE = 252
SH_OP = 0.15; SH_BLUR = 20; SH_DY = 24          # bóng đổ mềm phía dưới
CT_OP = 0.16; CT_BLUR = 26                       # bóng tiếp xúc (mặt bàn)
HALO_OP = 0.30; HALO_BLUR = 10; HALO_GROW = 1     # bóng mờ bo quanh sản phẩm
EV_SIG = 45; EV_K = 0.6; EDGE_CUT = 2                          # làm đều sáng


def logo_rgba(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    alpha = np.clip((255 - a.min(axis=2)) * 2.2, 0, 255)
    return Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), 'RGBA')


def product(src):
    im = Image.open(src).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    rgb = np.asarray(bg.convert('RGB')).astype(float)
    m = rgb.min(axis=2) < 248
    m = ndimage.binary_opening(m, iterations=1)
    lab, n = ndimage.label(m)
    if n > 1:                                    # bỏ hạt bụi nhỏ
        sz = ndimage.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, 1 + np.where(sz > sz.max() * 0.01)[0])
    m0 = m.copy()                                # chỉ phần có màu, để đo độ sáng
    m = ndimage.binary_closing(m, iterations=6)
    m = ndimage.binary_fill_holes(m)
    # bỏ dải bóng mờ có sẵn quanh mép ảnh gốc: chỉ giữ phần đủ đậm so với nền
    core = ndimage.binary_fill_holes(ndimage.binary_closing(np.asarray(Image.open(src).convert('L')) < 238, iterations=6))
    m = ndimage.binary_erosion(m & core, iterations=EDGE_CUT)
    lab, n = ndimage.label(m)
    if n > 1:
        sz = ndimage.sum(m, lab, range(1, n + 1)); m = lab == (1 + int(np.argmax(sz)))             # che phần bóng sáng bên trong sản phẩm
    ys, xs = np.where(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgb = rgb[y0:y1, x0:x1]; m = m[y0:y1, x0:x1]; m0 = m0[y0:y1, x0:x1]
    lum = rgb.mean(axis=2); sat = rgb.max(axis=2) - rgb.min(axis=2)
    sel = m0 & (lum >= np.percentile(lum[m0], 60)) & (sat < 40)
    mean = rgb[sel].mean(axis=0)
    rgb = rgb * (mean.mean() / mean)             # khử ám màu
    p = np.percentile(rgb.mean(axis=2)[m0], 88)
    rgb = rgb * (WHITE / p)                      # đồng bộ độ sáng vùng trắng
    # làm đều độ sáng vùng trắng (khử mảng tối/sáng do ánh đèn)
    lum = rgb.mean(axis=2); bright = m0 & (lum > 150)
    w = ndimage.gaussian_filter(bright.astype(float), EV_SIG) + 1e-6
    lb = ndimage.gaussian_filter(np.where(bright, lum, 0), EV_SIG) / w
    gain = np.clip((WHITE / np.maximum(lb, 1)) ** EV_K, 0.85, 1.35)
    rgb = np.where(bright[..., None], rgb * gain[..., None], rgb)
    rgb = 255 * np.power(np.clip(rgb, 0, 255) / 255, 0.85)
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    out.putalpha(alpha)
    return out


def process(src, dst, logo):
    pr = product(src); pr.thumbnail((FIT, FIT), Image.LANCZOS)
    can = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    x = (S - pr.width) // 2; y = (S - pr.height) // 2 - 10
    a = np.asarray(pr.getchannel('A')).astype(float) / 255
    # bóng mềm: hình sản phẩm dịch xuống, làm mờ
    sh = np.zeros((S, S)); sh[y + SH_DY:y + SH_DY + pr.height, x:x + pr.width] = a[:S - y - SH_DY] if y + SH_DY + pr.height > S else a
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(SH_BLUR))).astype(float) / 255 * SH_OP
    # bóng tiếp xúc: elip mờ sát mép dưới
    ct = Image.new('L', (S, S), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(ct).ellipse([x + pr.width * 0.12, y + pr.height - 22, x + pr.width * 0.88, y + pr.height + 26], fill=255)
    ct = np.asarray(ct.filter(ImageFilter.GaussianBlur(CT_BLUR))).astype(float) / 255 * CT_OP
    halo = np.zeros((S, S)); hb = ndimage.binary_dilation(a > 0.5, iterations=HALO_GROW)
    hh, ww = hb.shape; halo[y:y + hh, x:x + ww] = hb[:S - y, :S - x]
    halo = ndimage.gaussian_filter(halo, HALO_BLUR) * HALO_OP
    shade = np.clip(sh + ct + halo, 0, 0.35)
    base = np.full((S, S, 3), 255.0) * (1 - shade[..., None]) + np.array([150, 150, 155]) * shade[..., None]
    can = Image.fromarray(base.astype(np.uint8), 'RGB').convert('RGBA')
    can.alpha_composite(pr, (x, y))
    wm = logo.copy(); wm.thumbnail((WM_W, WM_W), Image.LANCZOS)
    wa = np.asarray(wm).astype(float); wa[..., 3] *= WM_OP
    wm = Image.fromarray(wa.astype(np.uint8), 'RGBA')
    can.alpha_composite(wm, ((S - wm.width) // 2, (S - wm.height) // 2))
    can.convert('RGB').save(dst, 'JPEG', quality=88, optimize=True)


if __name__ == '__main__':
    logo = logo_rgba(sys.argv[1]); outdir = sys.argv[2]
    for i, s in enumerate(sys.argv[3:], 1):
        process(s, f'{outdir}/{i:02d}.jpg', logo); print(f'{outdir}/{i:02d}.jpg')
