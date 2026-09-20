"""EP.01 콘티·프롬프트 생성. python build_prompts.py (episodes/ep01 에서 실행)"""
files = {}
files['conti.md'] = """# EP.01 「말하지 않은 마음까지 읽는 초능력자」

주인공 두부. 소품: 알록달록 선글라스 (렌즈 연두 `#B5E550`, 테 보라 `#8E5BC7`, 가로로 긴 역삼각형). 이번 편은 망토 없음. 표지 + 7컷.

| 컷 | 장면 | 내레이션 | 속마음·대사(합성) |
|---|---|---|---|
| 표지 | 선글라스를 쓰고 허공에 손가락질하는 씩씩한 두부 | 제목 | — |
| 1 | 선글라스 두부가 타워 꼭대기에 서 있고, 바닥의 회색 실루엣 군중에게서 속마음이 쉴 새 없이 올라옴 | 나는 사람들이 말하지 않아도 / 그들의 마음을 읽을 수 있다. | 군중 속마음 조각: 배고파 / 집 가고 싶다 / 괜찮은 척 중 / 쟤 왜 저래 / 월요일 싫어 |
| 2 | 두부가 우는 소라를 안아 줌 | 이 능력 덕분에 / 많은 이들로부터 환영을 받기도 하고 | 소라: 내 맘 알아 주는 건 너밖에 없어 |
| 3 | 급식실. 선글라스 두부와 시무룩한 탱자가 식판을 놓고 앉아 있고, 고양이 3인조가 아니꼬운 눈으로 옆을 지나감. 전원 여고생 교복 | 때로는 주류 무리의 반대를 무릅쓰고 / 소외되는 이에게 손 내미는 영웅적 면모도 보여 준다. | — |
| 4 | 패스트푸드 카운터. 찡그린 점원(물범), 반 넘게 남은 햄버거를 든 채 눈치 보는 두부. 벽시계 | 이 능력 때문에 필요 없는 눈치를 보거나 / 손해를 자처할 때도 많고 | 시계 위: 마감 시간 1시간 넘게 남음 · 점원: 아무 생각 없음 |
| 5 | 켜진 모니터에 고양이 3인조가 사이좋게 찍은 인스타 화면. 두부는 선글라스를 던져 놓고 이불에 파묻혀 욺 | 스스로의 마음을 돌보지 못하는 나를 미워하거나 / 지난 날의 영웅적인 선택들까지 후회하기도 한다. | 두부: 이건 초능력이 아니라 저주야... |
| 6 | 탱자와 소라가 선글라스를 쓰고 양쪽에서 우는 두부에게 달려옴 | 그렇지만 내가 나를 챙기지 못할 때면, / 항상 내가 지켜낸 사람들이 나를 지켜 줬다. | — |
| 7 | 둥지 안에 조연들이 작은 새처럼 들어가 위를 보고 조잘거리고, 선글라스 두부가 둥지를 내려다봄. 머리 위 하트 | 나는 앞으로도 사람들의 마음을 외면하지 않을 것이다. / 내가 건넨 손길들로 내 주변을 따뜻하게 할 수만 있다면. | CTA: 당신 곁의 두부를 태그해 주세요 |

톤: 1–3 밝음 → 4–6 저채도·먹구름 → 7 포인트 컬러 복귀. 참조: 두부·소라·탱자·점원 시트, `ref/lineup-*.png`, 고양이 3인조 시트, 깜자 2장. 프롬프트는 `build_prompts.py`가 만든다.
"""
HEADER = """Reference images:
- The FIRST image is the CHARACTER SHEET of Dubu, a cream-colored sheep. Reproduce this exact character design.
- Further character sheets / a size lineup may follow; the lineup image shows their relative sizes.
- The last two images are STYLE references only (the Korean instatoon dog "Kkamja"): copy its drawing grammar — wobbly hand-drawn black outline of uneven thickness, flat colors, no shading, simple emotion symbols (sweat drop, sparkles, tiny rain cloud, hearts) — but NOT its character or color.

Dubu design:
- cream #F6F2E6 body, ONE solid color everywhere including the face. No markings, no darker face, no inner-ear color
- 2-head-tall potato body with a soft cloud-shaped fluffy outline, stubby limbs, tiny tail, two small rounded ears sticking out sideways
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes

Prop of this episode, THE SUNGLASSES: a pair of wide, horizontally long sunglasses shaped like a downward-pointing triangle (flat top edge, lenses tapering to a point at the bottom), with lime-green #B5E550 lenses and a purple #8E5BC7 frame. Drawn flat, bold, simple.

"""
END = "\nNo text, no letters, no speech bubbles, no captions. Plain white background.\n"
cuts = {}
cuts['cover'] = "Draw ONE full-body Dubu, front view, wearing THE SUNGLASSES, standing confidently with feet apart and chest out, one arm raised high pointing an index finger up into the air like a hero declaring something, the other arm on the hip. Three or four tiny sparkles around. Character in the lower 60% of the image, the upper 40% must be completely empty white for a title." + END
cuts['cut1'] = "Scene: Dubu wearing THE SUNGLASSES stands on the very top of a tall, simple tower (a plain tall pillar-like tower drawn with the same wobbly outline, light gray), looking down. At the bottom of the image, a crowd of many small featureless people-shaped silhouettes in flat medium gray (no faces, no details). From the crowd, many thin wavy dashed lines rise upward toward Dubu, like signals streaming up. Dubu is small on top of the tower, calm dot eyes. Everything in the lower 60% of the image, the upper 40% empty white." + END
cuts['cut2'] = """Additional character: Sora, a slate gray #C2C6CA penguin, ONE solid color, tiny yellow #E8B24A beak and feet, short flipper arms, dot eyes, no mouth (see her sheet). Same height as Dubu.
Scene: Dubu wearing THE SUNGLASSES hugs Sora warmly, arms wrapped around her. Sora is crying: dot eyes with two thin tear streams, shoulders hunched, leaning into Dubu. Two tiny sparkles and one small heart above them. Both full body, standing, in the lower 60% of the image; the upper 40% empty white.""" + END
cuts['cut3'] = """Additional characters: Tangja, a yellow #F5E08C duck (flat orange #F0A83A bill and feet, small feather tuft on the head, see her sheet), same height as Dubu. And three cats of the same design, same size as Dubu, in pink #F2C9CF, lavender #D6CBE6 and mint #C5DCCB (see the cats sheet): small pointed ears, thin tail, dot eyes, no mouth.
ALL characters wear a simple girls' high-school uniform: white short-sleeve shirt and a navy #2E3A59 pleated skirt. Nothing else.
Scene: a school cafeteria. In the foreground, Dubu wearing THE SUNGLASSES and Tangja sit side by side at a long plain table with two metal lunch trays with food. Tangja is sulky: eyes as small downward dashes, head drooping, a tiny gray rain cloud above her. Dubu sits close beside her, calm. Behind them, the three cats walk past in a line, each glancing at the two with a cold side-eye (eyes as small sideways dashes). Whole scene in the lower 65% of the image, the upper 35% empty white.""" + END
cuts['cut4'] = """Additional character: a fast-food clerk, a blue gray #BCD0DA seal (blob body, no ears, flipper arms, dot eyes, no mouth, see the clerk sheet), same height as Dubu. The clerk wears a small white paper cap and a plain red #D9534F apron.
Scene: a fast-food counter. The clerk stands behind a plain counter on the right, arms limp, eyes as two small slightly furrowed dashes (a mild frown), staring blankly. On the left, Dubu wearing THE SUNGLASSES stands holding a hamburger that is more than half uneaten, glancing nervously at the clerk: dot eyes looking sideways, body slightly shrunk, one sweat drop, a tiny gray rain cloud above her. On the wall between them, a simple round wall clock. Muted, slightly desaturated colors. Scene in the lower 60% of the image, the upper 40% empty white.
No text, no letters, no numbers on the clock, no speech bubbles, no captions. Plain white background.
"""
cuts['cut5'] = "Scene: a gloomy room. On the left, a desk with a glowing computer monitor; the screen shows a simple photo of three cats (pink #F2C9CF, lavender #D6CBE6, mint #C5DCCB, same design as the cats sheet) standing close together happily with closed-arc eyes and a tiny sparkle, framed like a social media post (just a picture inside a rounded rectangle, no text, no icons). On the right, Dubu is buried in a lumpy pale blue blanket on the floor, only her head showing, crying: dot eyes with two thin tear streams. THE SUNGLASSES lie thrown on the floor in front of the blanket. A small gray rain cloud above Dubu. Muted, desaturated colors. Scene in the lower 60% of the image, the upper 40% empty white." + END
cuts['cut6'] = """Additional characters: Tangja, a yellow #F5E08C duck (orange bill and feet, feather tuft), and Sora, a slate gray #C2C6CA penguin (yellow beak and feet, flipper arms). Both same height as Dubu (see sheets and lineup).
Scene: Dubu sits in the middle on the floor, still crying (dot eyes with two thin tear streams), NOT wearing sunglasses. From the left, Tangja runs toward her with wings spread wide and small motion lines behind; from the right, Sora runs toward her with flippers out and motion lines. BOTH Tangja and Sora are wearing THE SUNGLASSES (lime-green lenses, purple frame, downward-triangle shape). Tiny sparkles begin to appear around Dubu. Scene in the lower 60% of the image, the upper 40% empty white.""" + END
cuts['cut7'] = """The lineup image shows Dubu's friends and family: a peach fox (Misook), a tan deer with two-pronged antlers (Deoksu), a light gray mouse with big round ears (Kong), a yellow duck (Tangja), a slate gray penguin (Sora), a warm brown hedgehog (Bamtol).
Scene: a large round bird's nest made of woven brown twigs sits at the bottom center. Inside the nest, these six characters are drawn very small, packed together like baby birds, all looking up with happy closed-arc eyes, little chatter marks (short curved lines) around their heads. Dubu, drawn larger and wearing THE SUNGLASSES, stands beside the nest leaning over it and looking down into it lovingly, one small heart floating above her head. A few tiny sparkles. Warm, bright colors. Scene in the lower 60% of the image, the upper 40% empty white.""" + END

import os
os.makedirs('prompts', exist_ok=True)
open('conti.md', 'w', encoding='utf-8', newline='\n').write(files['conti.md'])
open('prompts/_header.txt', 'w', encoding='utf-8', newline='\n').write(HEADER)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(HEADER + v)
print(sorted(os.listdir('prompts')))
