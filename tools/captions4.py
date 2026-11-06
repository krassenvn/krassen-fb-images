# -*- coding: utf-8 -*-
CTA = "📩 Nhắn tin để được tư vấn chi tiết và đúng size bồn cầu nhà bạn!"
HT = "#krasen #napboncau #naproiem #suachuanhacua"
HT_KS5 = "#krasen #napboncau #suachuanhacua"   # KS5 la nap thuong, khong rơi em -> bo #naproiem
C = {
"KS5": ["""KS5 – nắp bồn cầu 36×44cm cho bồn cầu 2 khối (két nước rời) 🚽
✅ Rộng 36cm, dài 44cm (chỉnh dài 43–45cm tính từ mũi nắp đến chân ốc)
✅ Màu trắng sữa phủ bóng, hạn chế trầy xước
✅ Nhựa PP nguyên sinh không ố màu, nặng 1kg bền chắc
Thay thế cho nhiều loại bồn phổ thông 2 khối (két nước rời): Viglacera, Linax, Inax (C117, C108…)""",
"""Bồn cầu 2 khối, két nước rời nhà bạn cần thay nắp? 🚽
KS5 rộng 36cm, dài 44cm, chỉnh dài 43–45cm tính từ mũi đến chân ốc.

Màu trắng sữa phủ bóng, hạn chế trầy xước. Nhựa PP nguyên sinh không ố màu, nặng 1kg bền chắc.

Thay thế được cho nhiều loại bồn phổ thông 2 khối: Viglacera, Linax, Inax (C117, C108…)""",
"""🚽 KS5 – nắp bồn cầu cho bồn 2 khối (két nước rời)
▪ Rộng 36cm, dài 44cm (chỉnh dài 43–45cm)
▪ Màu trắng sữa phủ bóng, hạn chế trầy xước
▪ Nhựa PP nguyên sinh không ố màu
▪ Nặng 1kg bền chắc
Dùng cho bồn phổ thông 2 khối: Viglacera, Linax, Inax (C117, C108…)"""],
"KVS600": ["""KVS600 – nắp bồn cầu cao cấp mũi nhọn chữ V, bản đặc biệt 37×47cm 🌟
✅ Rộng 37cm, dài 47cm (chỉnh dài 46–48cm tính từ mũi đến ngang 2 chân ốc vít)
✅ Phù hợp bồn cầu rộng 36–38cm, dài 46–48cm
✅ Rơi chậm không gây tiếng ồn, màu trắng sữa phủ bóng hạn chế trầy xước
✅ Nhựa PP nguyên sinh cao cấp không ố màu, nặng 1,8kg dày chắc chắn, bảo hành 2 năm
Tương thích Inax (AC3003, AC902VN…), TOTO (MS188, MS625…), American (VF1808E, VF2011…), Viglacera (V37, V39…), Caesar (CD1340, C1356PW…)""",
"""Bồn cầu nhà bạn rộng 36–38cm, dài 46–48cm? KVS600 bản đặc biệt dáng chữ V mũi nhọn rất vừa 👌
Nắp rộng 37cm, dài 47cm, chỉnh dài 46–48cm tính từ mũi đến ngang 2 chân ốc vít.

Rơi chậm không gây tiếng ồn, nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, hạn chế trầy xước, không ố màu. Nặng 1,8kg dày chắc chắn, bảo hành 2 năm.

Dùng được cho Inax (AC3003, AC902VN…), TOTO (MS188, MS625…), American (VF1808E, VF2011…), Viglacera (V37, V39…), Caesar (CD1340, C1356PW…)""",
"""🌟 KVS600 – nắp bồn cầu cao cấp chữ V, bản đặc biệt
▪ Rơi chậm, không gây tiếng ồn
▪ Rộng 37cm, dài 47cm (chỉnh dài 46–48cm)
▪ Phù hợp bồn cầu rộng 36–38cm, dài 46–48cm
▪ Nhựa PP nguyên sinh cao cấp, trắng sữa phủ bóng, không ố màu
▪ Nặng 1,8kg dày chắc chắn, bảo hành 2 năm
Phù hợp Inax (AC3003, AC902VN…), TOTO (MS188, MS625…), American (VF1808E, VF2011…), Viglacera (V37, V39…), Caesar (CD1340, C1356PW…)"""],
}
def full(code, i):
    return C[code][i].strip() + "\n" + CTA + "\n" + (HT_KS5 if code == 'KS5' else HT)
