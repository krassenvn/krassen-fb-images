# Cong cu dung anh (khong chay tren Facebook)
- cutout.py: tach nen trang, lam trang bong san pham (khong do bong).
- gen.py: dung anh 1080x1350 tu 5 mau (nen sang, khong khung, co logo, khong gia, CTA "Nhan tin de duoc tu van chi tiet").
  Can thu muc img/ chua <ten>_cut.png (tu cutout.py) va img/logo.jpg (copy tu tools/logo.jpg).
- captions.py: caption 12 ma (khong gia).
Anh nguon: thu muc SP NAP DRIVE tren may Mac cua nguoi dung. Danh sach dang bai: ../manifest.json.

## Ban moi (29/10/2026)
- Moi bai co 2 anh san pham (mat trong + mat mo nap): compose.py tao img/<MA>_pair.png tu danh sach PAIRS (ma, anh, goc xoay).
- Lam trang bong nhe va deu: bu phan sang toi dien rong (gaussian sigma 60, he so 0.6) roi gamma 0.72; khong con vet sang cheo; khong do bong.
