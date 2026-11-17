"""Ảnh cho bài 6 ảnh, kiểu ghép đôi: mỗi ảnh = 2 hình của CÙNG 1 mã (mặt dưới + mặt mở nắp),
xử lý màu/độ sáng y hệt skill bài 1 ảnh (compose.cut: tách nền min RGB>=250, làm đều sáng
gaussian 60 hệ số 0.6, gamma 0.72, KHÔNG đổ bóng), nền trắng, logo Krassen chìm nhỏ ở giữa.
Dùng: python3 make6pair.py logo.jpg <ảnh ra.jpg> <ảnh mặt dưới> <ảnh mở nắp>"""
import sys, os, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import cut

S = 1080; MAXW = 1000; MAXH = 900; GAP = 40; WM_W = 130; WM_OP = 0.10


def logo_rgba(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    alpha = np.clip((255 - a.min(axis=2)) * 2.2, 0, 255)
    return Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), 'RGBA')


def pair(paths):
    ims = [cut(p) for p in paths]
    H = 1000
    ims = [im.resize((max(1, int(im.width * H / im.height)), H), Image.LANCZOS) for im in ims]
    W = sum(i.width for i in ims) + GAP * (len(ims) - 1)
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x = 0
    for im in ims:
        cv.alpha_composite(im, (x, 0)); x += im.width + GAP
    k = min(MAXW / cv.width, MAXH / cv.height)
    return cv.resize((int(cv.width * k), int(cv.height * k)), Image.LANCZOS)


def make(logo_path, out, paths):
    pr = pair(paths)
    can = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    can.alpha_composite(pr, ((S - pr.width) // 2, (S - pr.height) // 2))
    wm = logo_rgba(logo_path); wm.thumbnail((WM_W, WM_W), Image.LANCZOS)
    wa = np.asarray(wm).astype(float); wa[..., 3] *= WM_OP
    wm = Image.fromarray(wa.astype(np.uint8), 'RGBA')
    can.alpha_composite(wm, ((S - wm.width) // 2, (S - wm.height) // 2))
    can.convert('RGB').save(out, 'JPEG', quality=88, optimize=True)


if __name__ == '__main__':
    make(sys.argv[1], sys.argv[2], sys.argv[3:])
