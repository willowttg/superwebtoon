"""조연 6인 표정 후보 시트를 세로로 합쳐 합본 1장을 만든다. python assets/samples/faces/compose.py"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
ROWS = [
    ("misook", "미숙 · 엄마 · 여우", "잔소리 = 걱정. 타박하는 듯하다가 제일 먼저 알아주는 사람"),
    ("deoksu", "덕수 · 아빠 · 사슴", "무뚝뚝, 말 대신 행동. 표정을 읽을 수 없지만 믿음직"),
    ("kong", "콩 · 남동생 · 쥐", "눈치 0, 직진, 밉지 않은 무신경"),
    ("tangja", "탱자 · 친구1 · 오리", "외향, 오지랖, 시끄럽고 밝음"),
    ("sora", "소라 · 친구2 · 펭귄", "더 조용하고 소심. 두부를 알아봐 주는 유일한 사람"),
    ("bamtol", "밤톨 · 남친 · 고슴도치", "겉은 가시, 속은 부드러움. 결정 대신 해 주는 T"),
]
W = 1400
CROP = (0, 150, 1536, 850)  # 원본에서 그림+캡션 영역
BAND = 64

font_b = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 30)
font_r = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 22)

rows = []
for name, title, desc in ROWS:
    im = Image.open(os.path.join(HERE, f"{name}-faces.png")).convert("RGB").crop(CROP)
    h = int(im.height * W / im.width)
    rows.append((im.resize((W, h), Image.LANCZOS), title, desc))

H = sum(BAND + r[0].height for r in rows) + 20
M = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(M)
y = 10
for im, title, desc in rows:
    d.line([(40, y + 4), (W - 40, y + 4)], fill=(230, 226, 218), width=2)
    d.text((48, y + 16), title, fill=(58, 55, 51), font=font_b)
    tw = d.textlength(title, font=font_b)
    d.text((48 + tw + 24, y + 24), desc, fill=(138, 131, 122), font=font_r)
    y += BAND
    M.paste(im, (0, y))
    y += im.height
out = os.path.join(HERE, "cast-faces-all.png")
M.save(out)
print("saved", out, M.size)
