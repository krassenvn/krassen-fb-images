# -*- coding: utf-8 -*-
import json, re
CTA = "📩 Nhắn tin để được tư vấn chi tiết và đúng size bồn cầu nhà bạn!"
HT = "#krasen #napboncau #naproiem #suachuanhacua"
_m = json.load(open('manifest.json'))
_P = {p['code']: p for p in _m['products']}
def renamed(old, new):
    return [c.replace(old, new) for c in _P[old]['captions']]
C = {
 'KS07U': renamed('KS04U', 'KS07U'),
 'KSV600': renamed('KVS600', 'KSV600'),
 'KS09U': [
"""KS09U – nắp bồn cầu chữ U kiểu chụp kín bệ ngồi, 36×46cm 🚽
✅ Rộng 36cm, dài 46cm (chỉnh dài 46–48cm tính từ mũi đến ngang 2 chân ốc vít)
✅ Phù hợp bồn cầu rộng 35–36cm, dài 46–48cm
✅ Nắp đậy chụp kín bệ ngồi, hạn chế nước làm ướt bệ ngồi khi sử dụng
✅ Rơi chậm không gây tiếng ồn, màu trắng sữa phủ bóng hạn chế trầy xước
✅ Nhựa PP nguyên sinh cao cấp không ố màu, nặng 1,4kg dày chắc chắn, bảo hành 1 năm
Phù hợp TOTO (CW162, CW163…), Viglacera (P1135, V199…), American Standard (VF2309, VF2781)…""",
"""Bồn cầu nhà bạn rộng 35–36cm, dài 46–48cm? KS09U chữ U kiểu chụp kín rất vừa 👌
Nắp rộng 36cm, dài 46cm, chỉnh dài 46–48cm tính từ mũi đến ngang 2 chân ốc vít. Kiểu nắp đậy chụp kín bệ ngồi, hạn chế nước làm ướt bệ ngồi khi sử dụng.

Rơi chậm không gây tiếng ồn, nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, hạn chế trầy xước, không ố màu. Nặng 1,4kg dày chắc chắn, bảo hành 1 năm.

Dùng cho TOTO (CW162, CW163…), Viglacera (P1135, V199…), American Standard (VF2309, VF2781)…""",
"""🚽 KS09U – nắp bồn cầu chữ U chụp kín bệ ngồi
▪ Kích thước 36×46cm, chỉnh dài 46–48cm
▪ Hạn chế nước làm ướt bệ ngồi khi sử dụng
▪ Rơi chậm, không gây tiếng ồn
▪ Nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, không ố màu
▪ Nặng 1,4kg dày chắc chắn, bảo hành 1 năm
Phù hợp bồn cầu rộng 35–36cm, dài 46–48cm: TOTO (CW162, CW163…), Viglacera (P1135, V199…), American Standard (VF2309, VF2781)…"""],
 'KS12VB': [
"""KS12VB – nắp bồn cầu vuông bo rơi chậm 34×45cm ◻️
✅ Rộng 34cm, dài 45cm (chỉnh dài 45–46cm tính từ mũi đến ngang 2 chân ốc vít)
✅ Phù hợp bồn cầu rộng 34–35cm, dài 45–46cm
✅ Rơi chậm không gây tiếng ồn, màu trắng sữa phủ bóng hạn chế trầy xước
✅ Nhựa PP nguyên sinh cao cấp không ố màu, nặng 1,2kg, bảo hành 1 năm
Phù hợp Ceravi (C304, C315) và các bồn cầu vuông bo cạnh""",
"""Bồn cầu vuông bo cạnh nhà bạn rộng 34–35cm, dài 45–46cm? KS12VB rất vừa 👌
Nắp rộng 34cm, dài 45cm, chỉnh dài 45–46cm tính từ mũi đến ngang 2 chân ốc vít.

Rơi chậm không gây tiếng ồn, nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, hạn chế trầy xước, không ố màu. Nặng 1,2kg, bảo hành 1 năm.

Dùng cho Ceravi (C304, C315) và các bồn cầu vuông bo cạnh.""",
"""◻️ KS12VB – nắp bồn cầu vuông bo rơi chậm
▪ Kích thước 34×45cm, chỉnh dài 45–46cm
▪ Rơi chậm, không gây tiếng ồn
▪ Nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, không ố màu
▪ Nặng 1,2kg, bảo hành 1 năm
Phù hợp bồn cầu rộng 34–35cm, dài 45–46cm: Ceravi (C304, C315) và các bồn vuông bo cạnh"""],
}
def full(code, i):
    t = C[code][i]
    return t if CTA in t else t + "\n" + CTA + "\n" + HT
if __name__ == '__main__':
    import sys
    for c in C:
        for i in range(3): print('=====', c, i); print(full(c, i))
