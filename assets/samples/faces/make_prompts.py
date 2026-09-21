"""조연 6인 기본 표정 후보 3안 프롬프트 생성. python assets/samples/faces/make_prompts.py"""
import os
HERE = os.path.dirname(__file__)
HEAD = """Reference images:
- The FIRST image is the CHARACTER to draw: {who}. Reproduce this exact character design in every figure.
- The SECOND image is a STYLE reference only (the Korean instatoon dog "Kkamja"): copy its pen-line grammar and simple emotion symbols - but NOT its character or color.

LINE QUALITY (most important):
- Black outline drawn with a felt-tip pen: SOLID, CONTINUOUS, fully opaque black. No gaps, no white specks, no grain, no texture, no dry-brush, no sketchy double lines, no broken strokes.
- The hand-drawn feel comes ONLY from the path of the line: gently wobbly, slightly uneven curves, thickness varying a little along the stroke. Not from any texture inside the line.
- Flat fill, no shading, no gradients, no paper texture, no noise.

{design}

This is a CONCEPT SHEET exploring 3 candidate DEFAULT (resting) faces that show the personality even when nothing is happening. Landscape, plain white background. ONE row of three large figures, evenly spaced, full body, front view, same plain standing pose unless the caption says otherwise, so the differences are in the face, ears and posture only. A thin gray English caption under each figure, exactly as written below. No other text, no swatches, no frames. NO rain cloud, no cloud of any kind. Never a mouth, never blush.

{concepts}
"""
C = {
"misook": ("a soft-orange fox named Misook (front view, top-left figure)",
"""Misook design (identical in all figures):
- soft orange #F6CA9E body, ONE solid color everywhere including face, ears, tail. No markings, no white chest, no dark ear tips, no dark paws
- 2-head-tall potato body, stubby limbs, large pointed triangular ears, one big bushy tail curling up beside the body
- face base: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes, no ribbon, no clothes, no props
- personality: the mom. Nags because she worries; scolds first, but is the first to notice when something is wrong. Brisk, capable, in charge""",
"""1. STERN BROWS - dot eyes with two short straight eyebrow strokes pressed low and flat just above the eyes, both hands on hips, tail up.
2. ONE BROW UP - dot eyes, one eyebrow stroke arched high and the other flat (skeptical, "I already know"), arms crossed.
3. TIRED LIDS - eyes drawn as two short flat horizontal dashes (half-closed, unimpressed), head tilted slightly, tail flicking with a small motion line."""),
"deoksu": ("a tan deer named Deoksu (front view, top-left figure)",
"""Deoksu design (identical in all figures):
- tan #EACEAA body, ONE solid color everywhere including face and ears. No spots, no white belly, no darker muzzle
- 2-head-tall potato body, stubby limbs, tiny tail, small upright ears, and a pair of SIMPLE TWO-PRONG antlers (each antler one stem with one short branch, tan with black outline), the same antlers in every figure
- face base: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- personality: the dad. Silent and stiff, shows love through actions instead of words (peels fruit, drives you home without a word). Unreadable but dependable""",
"""1. DASH EYES - eyes drawn as two short flat horizontal dashes (stoic, unreadable), arms straight down at the sides, standing very square and still.
2. HEAVY BROWS - dot eyes with two thick straight eyebrow strokes low over the eyes, shoulders slightly hunched, standing square.
3. PRETEND NOT LOOKING - dot eyes shifted slightly to one side as if secretly watching, body facing front, one hand tucked behind the back."""),
"kong": ("a light-gray mouse named Kong (front view, top-left figure)",
"""Kong design (identical in all figures):
- light gray #DED6DA body, ONE solid color everywhere including face and ears. No pink inner ears, no markings
- 2-head-tall potato body, stubby limbs, two BIG round ears on top of the head, one thin curly tail
- face base: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- personality: the little brother. Zero tact, says whatever he thinks instantly, charges straight ahead, never worried. Cheeky but not mean""",
"""1. WIDE EYES - eyes as slightly bigger round black dots wide open, ears perked straight up, body leaning forward eagerly.
2. SMUG ARCS - eyes as two closed upward-curving arcs (pleased with himself), chest puffed out, both hands on hips.
3. COCKED BROW - dot eyes with one eyebrow stroke raised high, one tiny sparkle beside the head, one foot stepping forward mid-stride, one arm swinging."""),
"tangja": ("a yellow duck named Tangja (front view, top-left figure)",
"""Tangja design (identical in all figures):
- yellow #F5E08C body, ONE solid color everywhere including face and wings. The ONLY other color is the small flat bill and the two small webbed feet in orange #F0A83A
- 2-head-tall potato body, stubby wing arms, tiny tail tuft, a small tuft of feathers on top of the head, no neck
- face base: two small black dot eyes set wide apart, a small flat orange bill instead of a nose, NO MOUTH (the bill is closed and flat), NO BLUSH, no eyelashes, no clothes, no props
- personality: the loud friend. Extroverted, nosy, bright, always excited, drags the shy hero outdoors. Big energy in a small body""",
"""1. GLOSSY EYES - eyes as bigger round black dots each with a tiny white highlight (bright, eager), one wing raised in a wave, two small sparkles.
2. HAPPY ARCS - eyes as two closed upward-curving arcs, head tilted, both wings spread wide open, the head tuft bouncing with a small motion line.
3. HIGH BROWS - round dot eyes with two eyebrow strokes floating high above (permanently amazed), both wings up, small motion lines around the body."""),
"sora": ("a slate-gray penguin named Sora (front view, top-left figure)",
"""Sora design (identical in all figures):
- slate gray #C2C6CA body, ONE solid color everywhere including face and belly (no white belly, no black back). The ONLY other color is the tiny beak and two small feet in yellow #E8B24A
- 2-head-tall rounded body, short flipper arms held close to the body, no neck, no ears, tiny tail
- face base: two small black dot eyes set wide apart, a tiny yellow beak instead of a nose, NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- personality: the quiet friend, even shyer than the hero. Speaks softly, avoids eye contact, but is the one person who truly sees the hero""",
"""1. DOWNCAST DOTS - dot eyes placed low as if looking at the floor, flippers pressed tight against the body, body leaning slightly back.
2. DROOPY ARCS - eyes as two small downward-curving arcs (soft, timid), body shrunk a little smaller, one small sweat drop beside the head.
3. UPWARD PEEK - dot eyes shifted up and to one side as if peeking at someone, both flippers held together in front, one tiny sparkle beside the head."""),
"bamtol": ("a warm-brown hedgehog named Bamtol (front view, top-left figure)",
"""Bamtol design (identical in all figures):
- warm brown #C9A582 body, ONE solid color everywhere including the face (no lighter face patch, no two-tone). The spikes are drawn ONLY as a zigzag outline around the back of the head and body; no lines or spikes drawn inside the body
- 2-head-tall rounded body, stubby limbs, small rounded ears, no tail
- face base: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- personality: the boyfriend. Prickly and blunt on the outside, soft on the inside. Makes plans, decides things for you, logical to a fault, secretly caring""",
"""1. SHARP BROWS - dot eyes with two straight eyebrow strokes angled down toward the center (stern, serious), arms crossed.
2. COOL LIDS - eyes as two short flat horizontal dashes (half-closed, composed), chin slightly raised, hands clasped behind the back.
3. SHARP BROWS + HIDDEN HEART - same stern angled eyebrows and dot eyes, standing stiffly, but one tiny pale pink outline heart floating low behind his back where he cannot see it."""),
}
for n, (who, design, concepts) in C.items():
    with open(os.path.join(HERE, f"{n}-faces-prompt.txt"), "w", encoding="utf-8") as f:
        f.write(HEAD.format(who=who, design=design, concepts=concepts))
print("ok")
