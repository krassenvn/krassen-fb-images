CTA = "📩 Nhắn tin để được tư vấn chọn đúng bộ xả cho bồn cầu nhà bạn!"
HT = "#krasen #boxa #phukienboncau #suachuanhacua"
C = {'BX10X20CM': [
"""🚽 Bộ xả Krassen BX10X20CM – nhựa ABS cao cấp, bảo hành 3 năm

Bộ xả nước cho bồn cầu liền khối, kích thước 10×20cm (cổ xả 10cm, cao 20cm).
✔ Nhựa ABS cao cấp, bề mặt phủ bóng
✔ Sản xuất tại Việt Nam
✔ Bảo hành 3 năm""",
"""💧 Bồn cầu liền khối xả yếu, rò nước? Có thể do bộ xả đã xuống cấp.

Krassen BX10X20CM là bộ xả 10×20cm bằng nhựa ABS cao cấp phủ bóng, lắp cho bồn cầu liền khối.
✔ Cổ xả 10cm, cao 20cm
✔ Sản xuất tại Việt Nam
✔ Bảo hành 3 năm""",
"""🛠️ Bộ xả Krassen BX10X20CM – phụ kiện nhỏ, dùng bền mỗi ngày

Dành cho bồn cầu liền khối, kích thước 10×20cm, làm từ nhựa ABS cao cấp phủ bóng.
✔ Sản xuất tại Việt Nam
✔ Bảo hành 3 năm"""]}
def full(code, i): return C[code][i] + "\n\n" + CTA + "\n" + HT
if __name__ == '__main__':
    for i in range(3): print(full('BX10X20CM', i), '\n-----')
