"""조연 6인 선 샘플·시트 프롬프트 생성.  python assets/samples/make_cast_prompts.py
산출: assets/samples/<이름>-line-sample-prompt.txt, <이름>-sheet-prompt.txt
"""
import os
HERE = os.path.dirname(__file__)

LINE = """LINE QUALITY (most important):
- Outline drawn with a soft PENCIL, about HALF as thick as the line in the reference image: a thin, fine line. Color is a very dark warm gray (not pure black), slightly matte with a faint soft pencil grain along the stroke, edges a little soft.
- The line is still CONTINUOUS and closed: no gaps, no broken strokes, no sketchy multiple overlapping strokes, no hatching, no smudges. One clean thin pencil path per edge.
- The hand-drawn feel comes from the gently wobbly, slightly uneven path and the pencil texture of the line itself. Pressure varies a little so the line is slightly thicker in places.
- Flat fill, no shading on the body, no gradients, no paper texture in the background, white background stays pure white."""

SAMPLE = """Reference image:
- The image is the CHARACTER to draw: {who}. Reproduce this exact body design and default face, but draw it with the thin pencil line described below instead of the thick marker line of the reference.

{line}

{design}

Draw exactly TWO large figures side by side on a plain white background, no text, no captions, no frames:
LEFT: full body, FRONT view, plain standing, arms hanging limply, default face.
RIGHT: full body, SIDE view (profile facing left), plain standing, default face seen in profile ({side_note}). NO mouth mark anywhere.
"""

SHEET = """Reference image:
- The image is the CHARACTER to draw: {who}, shown in front and side view with the default face. Reproduce this exact design and this exact thin pencil line quality in every figure. Emotion symbols (sweat drop, sparkles, hearts, motion lines) are drawn simply in the same thin line.

{line}

{design}
- Emotion symbols allowed: sweat drop, sparkles, motion lines, short vertical gloom lines, tears, tiny hearts. NO rain cloud, NO cloud of any kind anywhere on the sheet. Never a mouth, never blush.

Draw a CHARACTER REFERENCE SHEET, landscape, plain white background. THREE rows of four figures, evenly spaced, a thin gray English caption under each figure exactly as written below. No other text, no swatches, no props, no frames. Poses may be loose, exaggerated and comic; the body may squash, stretch, tilt or sprawl. Figures need not be the same size or stiffly upright.

Row 1, turnaround (full body, plain standing, default face, arms hanging limply):
FRONT; 3/4 VIEW; SIDE (profile facing left, {side_note}, no mouth mark); BACK (no face visible).

Row 2, comic action poses:
{row2}

Row 3, comic reaction poses:
{row3}
"""

CAST = {
"misook": dict(
    who="a soft-orange fox named Misook",
    side_note="one dot eye with its flat eyebrow stroke above it",
    design="""Misook design (identical in all figures):
- soft orange #F6CA9E body, ONE solid color everywhere including face, ears, tail. No markings, no white chest, no dark ear tips, no dark paws
- 2-head-tall potato body, stubby limbs, large pointed triangular ears, one big bushy tail curling up beside the body
- DEFAULT FACE: two small black dot eyes set wide apart; two short straight black eyebrow strokes pressed low and flat just above the eyes (stern, in charge). One small dark dot nose. NO MOUTH, NO BLUSH, NO EYELASHES of any kind, no ribbon, no clothes, no props
- The flat eyebrows appear in EVERY figure, even when the eyes change shape (dots, closed upward arcs, flat dashes, bigger round dots, ">.<")
- personality: the mom. Nags because she worries; scolds first, notices first. Brisk, capable, always moving""",
    row2="""POINTING (leaning forward, one arm stretched out pointing with a finger, other hand on hip, small motion lines by the pointing arm);
RUSHING (seen from the side, hurrying forward with quick short steps, tail streaming behind, motion lines, one sweat drop);
SIGH (shoulders dropped, arms hanging heavy, eyes as flat dashes, one sweat drop, body slightly slumped);
PEEKING (seen from a 3/4 back angle looking over her own shoulder, one eye visible, ears turned back, tail up).""",
    row3="""STARTLED (leaning back, eyes as bigger round dots, both hands up, two sweat drops, motion lines);
ARMS CROSSED (standing with arms crossed, chin slightly up, weight on one leg, tail flicking with a small motion line);
PATTING (crouching down low, one hand extended out at a low height as if patting a small child on the head, eyes as closed upward arcs);
SOFTENED (standing quietly with both hands clasped in front, eyes as closed upward arcs, one tiny sparkle beside the head).""",
),
"deoksu": dict(
    who="a tan deer named Deoksu",
    side_note="one short flat dash eye visible, small upright ear and both antlers visible",
    design="""Deoksu design (identical in all figures):
- tan #EACEAA body, ONE solid color everywhere including face and ears. No spots, no white belly, no darker muzzle
- 2-head-tall potato body, stubby limbs, tiny tail, small upright ears, and a pair of SIMPLE TWO-PRONG antlers (each antler one stem with one short branch, drawn tan with black outline), exactly the same antlers in every figure
- DEFAULT FACE: eyes drawn as two short flat horizontal black dashes set wide apart (stoic, unreadable), one small dark dot nose. NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- The dash eyes are his default in most figures. Only when a caption says so the eyes open into small round dots (surprise) or close into upward arcs (rare warmth)
- personality: the dad. Silent and stiff, shows love through actions instead of words. Unreadable but dependable""",
    row2="""HANDS BUSY (sitting on the floor, head bent down, both hands held together low in front as if carefully working on something small, dash eyes looking down);
WALKING AWAY (seen from behind, walking off, one hand raised in a small wave without turning around, tiny tail);
SQUARE NOD (standing very square, head tipped forward in a small nod, one short motion line above the head, arms straight at the sides);
PIGGYBACK (bent forward slightly with both arms reaching back as if carrying someone on his back, seen from the side, steady steps).""",
    row3="""STARTLED (eyes opened into small round dots, body leaning back a little, one sweat drop, otherwise still stiff);
SLEEPING (lying flat on his back with arms straight at the sides, dash eyes, two or three tiny curved motion lines drifting above the head - absolutely NO letters, NO "z" symbols, no text of any kind);
QUIET PRIDE (hands clasped behind the back, chest slightly out, dash eyes, one tiny sparkle beside the head);
WAITING (standing in profile with both hands behind the back, one foot tapping with a small motion line, dash eyes).""",
),
"kong": dict(
    who="a light-gray mouse named Kong",
    side_note="one closed upward-arc eye visible, one big round ear on top, curly tail behind",
    design="""Kong design (identical in all figures):
- light gray #DED6DA body, ONE solid color everywhere including face and ears. No pink inner ears, no markings
- 2-head-tall potato body, stubby limbs, two BIG round ears on top of the head, one thin curly tail
- DEFAULT FACE: eyes drawn as two closed upward-curving black arcs set wide apart (smug, pleased with himself), one small dark dot nose. NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- The smug arc eyes are his default. When a caption says so the eyes may open into round dots (wide), become ">.<" (hit), or flat dashes (bored)
- personality: the little brother. Zero tact, says whatever he thinks instantly, charges straight ahead, never worried. Cheeky but not mean""",
    row2="""DASHING (running straight toward the viewer, arms pumping, ears flapping back, motion lines behind, arc eyes);
POINTING LAUGH (leaning back, one finger pointing forward, other hand on belly, arc eyes, small motion lines by the head);
SPRAWLED (lying on his stomach on the floor, chin resting on both hands, feet kicked up behind, arc eyes);
SHRUG (both palms turned up at the sides, shoulders raised, head tilted, arc eyes).""",
    row3="""POP UP (popping up from the bottom edge of his space, only head and raised arms visible, eyes open as round dots, small motion lines);
BORED (slouched sitting on the floor leaning back on both hands, eyes as flat dashes, tail limp);
WHISPER (leaning sideways, one hand cupped beside the face, one eye an arc and the other a round dot, one tiny sparkle);
BONKED (body tilted as if just hit lightly, eyes as ">.<", ears askew, three small stars floating above the head; the outline of the head and body stays solid, closed and continuous - the impact is shown only by the stars and the tilt, no broken or dented lines).""",
),
"tangja": dict(
    who="a yellow duck named Tangja",
    side_note="one big round eye with its tiny white highlight visible, flat orange bill at the front, head tuft on top",
    design="""Tangja design (identical in all figures):
- yellow #F5E08C body, ONE solid color everywhere including face and wings. The ONLY other color is the small flat bill and the two small webbed feet in orange #F0A83A
- 2-head-tall potato body, stubby wing arms, tiny tail tuft, a small tuft of feathers on top of the head, no neck
- DEFAULT FACE: eyes as two round black dots slightly bigger than usual, each with one tiny white highlight dot (bright, eager, glossy), set wide apart; a small flat orange bill instead of a nose, closed and flat. NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- The glossy highlight eyes are her default. When a caption says so the eyes may become closed upward arcs (delight), bigger round dots (shock), or ">.<"
- personality: the loud friend. Extroverted, nosy, bright, always excited, drags the shy hero outdoors. Big energy in a small body""",
    row2="""BOTH WINGS UP (jumping with both wings raised high, feet off the ground, glossy eyes, sparkles);
DRAGGING (seen from the side so only ONE eye is visible, leaning far forward pulling hard on something off to the side with both wings gripping, feet dug in, motion lines; the visible eye is a single round black dot with its white highlight, drawn normally);
CHATTERING (leaning forward toward the viewer, both wings gesturing in the air, glossy eyes, several short motion lines around the head);
POINTING FAR (one wing pointing up and out into the distance, other wing on the hip, glossy eyes, one sparkle).""",
    row3="""RUNNING HUG (running toward the viewer with both wings spread wide open, eyes as closed upward arcs, motion lines);
FLOPPED HAPPY (lying on her back with wings and feet in the air, eyes as closed upward arcs, two sparkles);
SHOCKED (leaning back, eyes as bigger round dots with highlights, both wings up, two sweat drops);
GOSSIP (leaning sideways with one wing cupped beside the bill, eyes shifted to the side, one tiny sparkle).""",
),
"sora": dict(
    who="a slate-gray penguin named Sora",
    side_note="one small dot eye placed low as if looking down, tiny yellow beak at the front",
    design="""Sora design (identical in all figures):
- slate gray #C2C6CA body, ONE solid color everywhere including face and belly (no white belly, no black back). The ONLY other color is the tiny beak and two small feet in yellow #E8B24A
- 2-head-tall rounded body, short flipper arms held close to the body, no neck, no ears, tiny tail
- DEFAULT FACE: two small black dot eyes set wide apart and placed slightly LOW on the face as if looking down at the floor (downcast, shy); a tiny yellow beak instead of a nose. Flippers pressed tight against the body. NO MOUTH, NO BLUSH, no eyelashes, no clothes, no props
- The low downcast dot eyes are her default. When a caption says so the eyes may become small closed upward arcs (quiet joy), dots shifted up/sideways (peeking), bigger dots (startled), or dots with tear streams
- personality: the quiet friend, even shyer than the hero. Speaks softly, avoids eye contact, but is the one person who truly sees the hero""",
    row2="""SHRINKING (body squashed down smaller and rounder, flippers pressed together in front, downcast eyes, one sweat drop);
SMALL NOD (standing, head tipped slightly down in a tiny nod, one very short motion line above, flippers tight);
PEEK UP (eyes shifted up and to one side as if peeking at someone, flippers held together in front, body turned slightly away);
SITTING (sitting on the floor with both flippers resting on the ground beside her, looking down, tiny tail visible).""",
    row3="""QUIET TEARS (standing still, one thin tear line running from each eye, flippers tight, no other motion);
SMALL JOY (eyes as two tiny closed upward arcs, flippers lifted slightly away from the body, one small sparkle);
STARTLED (little hop off the ground, eyes as bigger round dots, flippers out, one sweat drop, small motion lines);
FIDGET (flippers rubbing together in front, eyes shifted sideways, body leaning slightly back, one tiny sweat drop).""",
),
"bamtol": dict(
    who="a warm-brown hedgehog named Bamtol",
    side_note="one dot eye inside its round glasses rim seen from the side as a thin circle, no temple arm going to the ear",
    design="""Bamtol design (identical in all figures):
- warm brown #C9A582 body, ONE solid color everywhere including the face (no lighter face patch, no two-tone). The spikes are drawn ONLY as a zigzag outline around the back of the head and body; no lines or spikes drawn inside the body
- 2-head-tall rounded body, stubby limbs, two small rounded ears at the top sides of the head (in the BACK view the same two small rounded ears sit at the top of the head, drawn as simple half-circles inside the zigzag spike outline), no tail
- DEFAULT FACE: two small black dot eyes set wide apart, one small dark dot nose, and ROUND GLASSES: one thin black circular rim drawn around each eye, the two rims joined by one short bridge line over the nose. NOTHING ELSE - no temple arms, no pieces going to the ears, the rims simply sit on the face. Lenses are transparent (body color shows inside). NO MOUTH, NO BLUSH, no eyelashes, no clothes, no other props
- The round glasses appear in EVERY figure, including side and 3/4 views (in profile the near rim is a thin circle on the face). Inside the rims the eyes may change: dots, closed upward arcs, flat dashes, bigger round dots
- personality: the boyfriend. Prickly and blunt on the outside, soft on the inside. Makes plans, decides things for you, logical to a fault, secretly caring""",
    row2="""ARMS CROSSED (standing with arms crossed, chin slightly up, dot eyes behind the glasses);
MAKING A POINT (one finger raised beside the head as if explaining a plan, other hand on hip, small motion lines by the finger);
GLASSES PUSH (one hand pushing the bridge of the glasses up the nose, eyes as flat dashes, one small sparkle glinting on a rim);
STRIDING (seen from the side, walking briskly with purpose, arms swinging, motion lines behind; the one visible eye is a SOLID black dot inside its round rim, drawn as dark as every other eye on the sheet).""",
    row3="""CURLED BALL (rolled into a round ball on the floor with the zigzag spike outline all around, only the glasses and dot eyes showing at the front);
STARTLED (leaning back, glasses tilted slightly askew on the face, eyes as bigger round dots, one sweat drop);
THINKING (sitting on the floor, chin resting on one hand, elbow on knee, dot eyes behind the glasses, one very short line above the head);
SOFT MOMENT (standing stiffly facing front with both hands behind the back, eyes as closed upward arcs behind the glasses, one tiny pale pink outline heart floating low behind his back).""",
),
}

for n, c in CAST.items():
    with open(os.path.join(HERE, f"{n}-line-sample-prompt.txt"), "w", encoding="utf-8") as f:
        f.write(SAMPLE.format(line=LINE, **c))
    with open(os.path.join(HERE, f"{n}-sheet-prompt.txt"), "w", encoding="utf-8") as f:
        f.write(SHEET.format(line=LINE, **c))
print("ok")
