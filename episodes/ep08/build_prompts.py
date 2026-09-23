"""EP.08 프롬프트 생성. 저장소 루트에서 python episodes/ep08/build_prompts.py. 콘티는 conti.md 직접 편집."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
S = os.path.join(ROOT, "assets", "samples")


def block(name):
    """시트 프롬프트의 LINE QUALITY + design 블록."""
    t = open(os.path.join(S, f"{name}-sheet-prompt.txt"), encoding="utf-8").read()
    return t[t.index("LINE QUALITY"):t.index("\nDraw a CHARACTER")].strip() + "\n"


LINE = block("dubu").split("\n\n")[0] + "\n\n"

# 점원 시트 프롬프트는 구형식이라 design 블록을 여기서 직접 정의
CLERK = """Clerk design (identical in all figures):
- blue gray #BCD0DA body, ONE solid color everywhere including face and belly. No markings, no spots
- 2-head-tall soft blob SEAL body, no neck, no ears, two short flipper arms, a small flat tail flipper at the bottom instead of legs
- DEFAULT FACE: two small black dot eyes set wide apart, one small dark dot nose. NO MOUTH, NO BLUSH, no eyelashes, no whiskers
- personality: a part-time shop clerk with a blank, empty stare; polite, slow, harmless. In this picture she wears one small flat dark-green #4F7A5A shop apron with NO letters on it
- Emotion symbols allowed: sweat drop, sparkles, motion lines. NO rain cloud, NO cloud of any kind. Never a mouth, never blush.
"""

# 이 편의 초능력 소품 — ref/dubu-battery-sheet-prompt.txt 의 소품 블록과 동일
BATTERY = """BATTERY PACK prop (Dubu wears it, exactly as on the battery-pack sheet):
- a small round backpack shaped like a chunky AA BATTERY, worn on Dubu's back with two thin black-outlined straps over her shoulders. Battery body in vivid electric blue #2F7CF6 with a big bright yellow #FFD600 LIGHTNING-BOLT emblem and a small yellow #FFD600 cap sticking up at the top
- from the bottom of the battery comes a bright yellow #FFD600 COILED spiral cable ending in a chunky yellow two-prong PLUG. When she is charging the plug is inserted into a small white wall outlet; otherwise the plug dangles or drags on the ground behind her
- bright glossy-flat colors, thick outline. No letters, no numbers, no percent signs on it
"""


def design(name):
    if name == "clerk":
        return CLERK
    if name == "battery":
        return BATTERY
    return block(name).split("\n\n", 1)[1]


STYLE = "Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes only). Reproduce these exact character designs and this exact line quality. Cute, small, harmless mood.\n\n"
LAYOUT = " Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = "\nNo text, no letters, no numbers, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies. NO rain cloud anywhere.\n"


def head(*names):
    return STYLE + LINE + "".join(design(n) + "\n" for n in names)


cuts = {}
cuts["cover"] = head("dubu", "battery") + (
    "Camera: front view, slightly from the side. At home, Dubu sits on the floor leaning back comfortably against a small flat round cushion, short legs stretched out in front of her, "
    "eyes as closed upward arcs (blissful, recharging) with her worried eyebrows, three small sparkles above her head. "
    "She wears her BATTERY PACK; its yellow coiled cable runs from the pack to a white double wall outlet on the wall behind her and the yellow plug is inserted, so she is charging. "
    "A second thin white cable runs from the same outlet to a smartphone lying face-up on the floor right beside her, charging too, so the sheep and the phone are charging side by side. "
    "Nothing else in the picture." + LAYOUT) + END

cuts["cut1"] = head("dubu") + (
    "Camera: LOW ANGLE from floor level, side view, inside a living room. "
    "In the foreground on the floor lies a smartphone face-up, RINGING: drawn with bold vibration motion lines on both sides and three small curved sound-wave arcs above it; "
    "its screen shows only one plain green circle and one plain red circle, no letters. "
    "Behind it stands a small flat sofa in muted olive color, seen from the side. Dubu hides BEHIND the sofa armrest: only the top of her head, her two drooping ears, her worried eyebrows and two dot eyes peek over the armrest, "
    "both hands gripping the edge of the armrest, the rest of her body hidden. Two sweat drops fly off her head. "
    "Flat simple colors." + LAYOUT) + END

cuts["cut2"] = head("dubu", "battery") + (
    "Camera: FROM BEHIND Dubu, over her shoulder, inside an apartment entrance hallway. "
    "A flat front door in muted beige with a round peephole fills the middle of the picture; the peephole sits a little above Dubu's eye height. "
    "Dubu, seen from the back, stands on TIPTOE pressed flat against the door, one eye against the peephole, both hands flat on the door beside her head, "
    "her two ears raised straight up alertly, one sweat drop beside her head. She wears her BATTERY PACK, fully visible from behind, its yellow plug dangling down behind her. "
    "On the floor by the door two pairs of small shoes lie scattered. Nothing else in the picture." + LAYOUT) + END

cuts["cut3"] = head("dubu", "clerk") + (
    "Camera: front view, eye level, inside a clothing shop. "
    "On the LEFT stands a clothes rack (a simple metal rail on legs) tightly packed with many hanging clothes in muted colors (beige, gray, navy, dusty pink). "
    "From the middle of the hanging clothes only Dubu's two drooping ears and the top of her head with her worried eyebrows and two dot eyes are still visible; "
    "the rest of her body has already disappeared backward INTO the clothes, with a few short motion lines showing her sinking backward between the hangers. "
    "On the RIGHT the seal clerk in a small flat dark-green apron walks toward the rack, one flipper raised politely, dot eyes, one tiny sparkle beside her head. "
    "The lineup image shows their relative sizes only." + LAYOUT) + END

cuts["cut4"] = head("dubu", "battery", "tangja") + (
    "Camera: HIGH ANGLE, looking down at a sidewalk from above. A flat light-gray sidewalk band runs from the bottom to the top of the picture. "
    "Tangja the duck walks AWAY along the sidewalk toward the top of the picture, seen from behind and above, one wing raised high in a goodbye wave, head turned slightly back, eyes as closed happy arcs; her body must be the PALE soft yellow #F5E08C exactly, not a brighter or more saturated yellow. "
    "In the lower foreground Dubu hugs a tall dark-gray street LAMPPOST with both arms, her whole body pressed flat behind the pole trying to hide, "
    "only her head peeking out around the pole toward Tangja with dot eyes and worried eyebrows, ears drooping, one sweat drop. "
    "She wears her BATTERY PACK; the blue battery and its yellow plug stick out from behind the pole, giving her away. "
    "The lineup image shows their relative sizes only." + LAYOUT) + END

cuts["cut5"] = head("dubu", "battery", "kong") + (
    "Camera: SIDE VIEW at floor level, inside an apartment entrance, the closed front door at the far left. "
    "Dubu lies completely FLAT on her belly on the floor just inside the door, arms and legs spread out limp, her face turned toward the camera resting on the floor, "
    "eyes as two tired flat dashes with her worried eyebrows, ears flopped onto the floor. "
    "She wears her BATTERY PACK on her back; its yellow coiled cable stretches up from the pack to a white wall outlet on the wall behind her and the yellow plug is inserted, so she is charging where she fell; three small sparkles rise above her. "
    "Her shoes lie kicked off beside her and a small bag is dropped on the floor. "
    "On the RIGHT Kong the mouse stands looking down at her, eyes as closed smug arcs, holding an empty bowl in one hand and a spoon in the other. "
    "The lineup image shows their relative sizes only." + LAYOUT) + END

for n, p in cuts.items():
    with open(os.path.join(HERE, "prompts", f"{n}.txt"), "w", encoding="utf-8") as f:
        f.write(p)
print("ok", list(cuts))
