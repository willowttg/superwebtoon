"""엑스트라(고양이 3인조·점원) 선 샘플·시트 프롬프트 생성.  python assets/samples/make_extra_prompts.py"""
import os, re
HERE = os.path.dirname(__file__)
LINE = re.search(r'LINE = """(.*?)"""', open(os.path.join(HERE, "make_cast_prompts.py"), encoding="utf-8").read(), re.S).group(1)

CATS_DESIGN = """Draw THREE CATS, a trio of popular classmates. All three share the same design except body color:
- 2-head-tall potato body, head bigger than body, stubby limbs, one thin short tail, small pointed triangular cat ears
- ONE solid body color everywhere including the face and the INSIDE of the ears (the ears are the same flat color as the body - no lighter or darker inner-ear shape). No markings, no stripes, no patches
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
- blank, slightly dazed expression by default; arms hanging limply; small, scrappy, harmless mood
- no eyelashes, no ribbon, no clothes, no accessories, no props
Cat A: pink #F2C9CF. Cat B: lavender #D6CBE6. Cat C: mint #C5DCCB."""

CLERK_DESIGN = """The character is a SEAL, a part-time fast-food clerk, drawn without uniform here:
- blue gray #BCD0DA body, ONE solid color everywhere including face and belly. No markings, no spots
- 2-head-tall soft blob body, no neck, no ears, two short flipper arms, a small flat tail flipper at the bottom instead of legs
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
- completely blank, empty stare by default - thinking about nothing; arms hanging limply; small, harmless mood
- no eyelashes, no whiskers, no clothes, no accessories, no props"""

HEAD_SAMPLE = """Reference images:
- The FIRST image is the CHARACTER design reference (a sheet from this project). Reproduce the {what} from it exactly.
- The SECOND image is a LINE STYLE reference only (a cream sheep): copy its thin grainy pencil line texture exactly - but NOT its character, shape or color.

{line}

{design}

{layout} Plain white background, no text, no captions, no frames. NO mouth mark anywhere.
"""

HEAD_SHEET = """Reference images:
- The FIRST image is the CHARACTER design reference: {what} drawn with the correct thin pencil line. Reproduce this exact design and line quality in every figure.
- The SECOND image is a LINE STYLE reference only (a cream sheep): copy its thin grainy pencil line texture exactly in every figure - but NOT its character, shape or color. Emotion symbols (sweat drop, sparkles, motion lines) are drawn simply in the same pencil line.

{line}

{design}

{sheet}
"""

CATS_SHEET = """Draw a CHARACTER REFERENCE SHEET, landscape, plain white background. Three rows (one per cat, A on top, then B, then C), five figures per row, evenly spaced, every figure the same size and proportions, a thin gray English caption under each figure. No other text, no swatches, no props, no frames. NO rain cloud, no cloud of any kind.
Each row, full body: FRONT, 3/4 VIEW, SIDE, BACK, SIDE-EYE (front view, eyes as two small dashes tilted to look sideways in a cold judging glance, head slightly turned away, arms limp)."""

CLERK_SHEET = """Draw a CHARACTER REFERENCE SHEET, landscape, plain white background. Two rows, evenly spaced, every figure the same size and proportions, a thin gray English caption under each figure. No other text, no swatches, no props, no frames. NO rain cloud, no cloud of any kind.
Row 1, turnaround (full body, upright, blank face): FRONT, 3/4 VIEW, SIDE, BACK.
Row 2, expressions (full body, front view). Since the seal has no mouth, show emotion only with the eyes, posture and symbols:
NEUTRAL (dot eyes, flippers limp);
BORED (eyes as small half-closed dashes, body slouching);
SURPRISED (eyes as slightly bigger round dots, body leaning back, sweat drop);
HAPPY (eyes as closed upward arcs, one tiny sparkle);
TIRED (dot eyes, body leaning to one side, one sweat drop);
POINTING (one flipper raised sideways as if pointing at something, dot eyes)."""

files = {
    "cats-line-sample-prompt.txt": HEAD_SAMPLE.format(what="three cats (silhouette, ears, tail)", line=LINE, design=CATS_DESIGN,
        layout="Draw exactly FOUR large figures in one row: Cat A FRONT view, Cat B FRONT view, Cat C FRONT view, then Cat A SIDE view (profile facing left, one dot eye visible). Plain standing, arms hanging limply."),
    "clerk-line-sample-prompt.txt": HEAD_SAMPLE.format(what="SEAL (blob body, no ears, flipper limbs)", line=LINE, design=CLERK_DESIGN,
        layout="Draw exactly TWO large figures side by side: LEFT full body FRONT view, RIGHT full body SIDE view (profile facing left, one dot eye visible). Upright, flippers hanging limply, blank face."),
    "cats-sheet-prompt.txt": HEAD_SHEET.format(what="three cats", line=LINE, design=CATS_DESIGN, sheet=CATS_SHEET),
    "clerk-sheet-prompt.txt": HEAD_SHEET.format(what="a seal", line=LINE, design=CLERK_DESIGN, sheet=CLERK_SHEET),
}
for name, text in files.items():
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(text)
print("ok")
