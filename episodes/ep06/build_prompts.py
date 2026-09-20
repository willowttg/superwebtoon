"""EP.06 프롬프트 생성. python build_prompts.py (episodes/ep06 에서 실행). 콘티는 conti.md 직접 편집."""
import os

STYLE = """Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes). Reproduce these exact character designs. Drawing grammar: wobbly hand-drawn black outline of uneven thickness, flat colors, no shading, simple emotion symbols. Cute, small, harmless mood.

"""
TANGJA = """Tangja design (THE MAIN CHARACTER of this episode, a yellow duck):
- yellow #F5E08C body, ONE solid color everywhere including face and wings. The ONLY other color is the small flat bill and the two small webbed feet in orange #F0A83A
- 2-head-tall potato body, stubby wing arms, tiny tail tuft, a small tuft of feathers on top of the head, no neck
- face: two small black dot eyes set wide apart, a small flat orange bill instead of a nose, NO MOUTH, NO BLUSH, no eyelashes
"""
DUBU = """Dubu design (Tangja's friend, a cream sheep, same height as Tangja):
- cream #F6F2E6 body, ONE solid color everywhere including the face. No markings, no darker face, no inner-ear color
- 2-head-tall potato body with a soft cloud-shaped fluffy outline, stubby limbs, tiny tail, two small rounded ears sticking out sideways
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes
"""
SORA = """Sora design (Tangja's friend, a slate-gray penguin, same height as Tangja):
- slate gray #C2C6CA body, ONE solid color everywhere including the belly. The ONLY other color is the tiny beak and the two small feet in yellow #E8B24A
- 2-head-tall rounded body, short flipper arms held close to the body, no neck, no ears, tiny tail
- face: two small black dot eyes set wide apart, a tiny yellow beak instead of a nose, NO MOUTH, NO BLUSH
"""
CAP = """Prop of this episode, THE CAP: a flat hot-pink #E91E8C graduation mortarboard cap (square flat top, small round crown) with a sky-blue #4FC3F7 tassel hanging from one corner, sitting on top of Tangja's head over her feather tuft. Drawn flat and bold, no shading.
"""
DIPLOMA = "a diploma: a rolled cream-colored paper scroll tied around the middle with a red ribbon"
TAG = "each item has a small white rectangular price tag on a short string still attached (blank, no letters)"
GEAR = ("brand-new hobby gear, " + TAG + ": an acoustic guitar, a rolled purple yoga mat, a folded camping chair, a ball of red yarn with two knitting needles, "
        "a small film camera, a pair of inline skates, a small green one-person tent (packed in its bag), a pair of dumbbells, a small ukulele")
SURFBOARD = "a sky-blue #4FC3F7 surfboard with one white stripe down the middle"
CROWD = "several small featureless people-shaped silhouettes in flat medium gray #9A9A9A, no faces, no details"
LAYOUT = "Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = "\nNo text, no letters, no numbers, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.\n"


def head(*designs):
    return STYLE + "".join(designs) + "\n"


cuts = {}
cuts['cover'] = head(TANGJA, CAP) + (
    "Front view. Draw ONE full-body Tangja wearing THE CAP, standing with feet apart, chest out, in a proud hero pose: "
    "her LEFT wing rests on her hip, and her RIGHT wing is raised straight up high, clearly attached at the shoulder, holding " + DIPLOMA + " up like a trophy. "
    "Eyes as two closed happy upward arcs. At her feet on the ground lies an acoustic guitar with a small blank white price tag still attached. "
    "Behind her, thin light-gray radial light rays fan out from behind her body, and several small sparkles float around the diploma. "
    "Character and guitar in the lower 60% of the image; the upper 40% must be completely empty white for a title.") + END

cuts['cut1'] = head(TANGJA, CAP) + (
    "Camera: LOW ANGLE, seen from floor level looking slightly up, so Tangja looks tall and triumphant. "
    "Tangja wears THE CAP and walks from left to right in side view with her chest out, an acoustic guitar slung on her back by a strap (blank price tag still hanging from its neck), "
    "and " + DIPLOMA + " tucked under one wing. Eyes as two closed happy upward arcs, one small black music note floating above her head. "
    "On the floor behind her lies a small flat wall calendar: a plain white page with a grid of empty squares and NO numbers; the first three squares of the top row are crossed out with big red X marks, all other squares are empty. "
    "Bright, warm colors. " + LAYOUT) + END

cuts['cut2'] = head(TANGJA, DUBU) + (
    "Camera: SIDE VIEW. An indoor climbing wall is a TALL VERTICAL flat pale-gray panel standing on the RIGHT side of the picture, seen edge-on from the side, "
    "rising straight up from the floor to the top of the drawn area; its left face is dotted with round climbing holds in flat red, blue, yellow and green. "
    "Both characters cling to the LEFT face of this wall in profile, facing right toward the wall. "
    "Tangja is HIGH UP near the top of the wall, gripping a hold with one wing, her other wing stretched down and back toward Dubu, waving; eyes as two closed happy upward arcs. "
    "Dubu is at the very BOTTOM of the wall, gripping the lowest hold with both hands, her feet only just off the floor, body pressed against the wall, eyes as two closed happy upward arcs (scared but having fun), one big sweat drop beside her head. "
    "Both wear a simple flat orange climbing harness around the waist. No cap in this scene. No contact-shadow ellipses in this picture (both characters are on the wall). Bright colors. " + LAYOUT) + END

cuts['cut3'] = head(TANGJA, SORA) + (
    "Camera: seen from behind Sora, 3/4 over her shoulder. Sora is in the LEFT foreground, larger and seen from the back-side, facing into the room. "
    "In front of her Tangja (no cap) has just swung open the two doors of a tall flat wardrobe, and the wardrobe is packed full of " + GEAR + ", stacked on shelves. "
    "Tangja holds out a small film camera (blank price tag hanging from it) toward Sora with both wings, eyes as two closed happy upward arcs. "
    "One small heart floats above Sora's head. The lineup image shows their relative sizes only. Bright, warm colors. " + LAYOUT) + END

cuts['cut4'] = head(TANGJA, CAP) + (
    "Camera: front view from slightly above, looking down into Tangja's room. "
    "On the floor is a big messy mountain of " + GEAR + ", piled up and spilling sideways, all in MUTED desaturated colors. "
    "On top of the pile sits Tangja wearing THE CAP, tearing open a large brown cardboard box in front of her; " + SURFBOARD + " sticks halfway out of the box, and the surfboard is the ONLY vivid saturated color in the picture. "
    "Both her wings are thrown up in excitement, eyes as two closed happy upward arcs, several short black motion lines radiate around her head. "
    "Keep a little empty space above the guitar and above the tent for labels. Overall colors muted and low-saturation except the surfboard. " + LAYOUT) + END

cuts['cut5'] = head(TANGJA) + (
    "Camera: EXTREME CLOSE-UP. Only Tangja's two yellow wings are visible at the bottom, holding a smartphone upright and filling most of the lower picture; no head, no body. "
    "The phone screen shows a second-hand marketplace app: at the top one empty rounded search bar (blank), below it a vertical list of four listings, each a row with a square photo on the left and two short blank gray bars on the right. "
    "The four photos are: an acoustic guitar, a rolled purple yoga mat, a small green tent bag, a pair of inline skates. No letters or numbers anywhere on the screen. "
    "One small black scribbled swirl (a messy scribble, like a doodle) floats in the air just above the phone. Colors muted and desaturated. " + LAYOUT) + END

cuts['cut6'] = head(TANGJA, CAP) + (
    "Camera: from INSIDE the room, behind Tangja. Night. Tangja is seen from the BACK, standing at a large flat window (simple dark-blue #2B3A5C night sky in the window frame), "
    "one wing holding THE CAP down at her side (not on her head), her feather tuft visible, head slightly drooping, one small gray rain cloud floating above her head. "
    "Through the window, outside on the street, " + CROWD + " run in a line from left to right, all in the same running pose, like a nightly running crew. "
    "To one side inside the room, a low heap of hobby gear (guitar, yoga mat, tent) drawn all in flat gray. Colors muted and dim. " + LAYOUT) + END

cuts['cut7'] = head(TANGJA, DUBU, CAP) + (
    "Camera: SIDE VIEW, both characters running from left to right. Daytime, plain white background with only a thin gray ground line. "
    "Tangja in front wears THE CAP and a terracotta #C77B3F hero cape knotted at the front of her neck and streaming behind her, " + SURFBOARD + " tucked under one wing, "
    "and with the other wing she grips Dubu's wrist, pulling her along. Eyes as two closed happy upward arcs. "
    "Dubu behind her is being dragged along mid-run, leaning back a little, her free hand holding a small pink chalk bag on a string, eyes as two closed happy upward arcs. "
    "A few small black five-point stars float in the air behind them (no sparkles, no motion lines). Bright, warm colors. The lineup image shows their relative sizes only. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
