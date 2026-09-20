"""EP.05 프롬프트 생성. python build_prompts.py (episodes/ep05 에서 실행). 콘티는 conti.md 직접 편집."""
import os

STYLE = """Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes). Reproduce these exact character designs. Drawing grammar: wobbly hand-drawn black outline of uneven thickness, flat colors, no shading, simple emotion symbols. Cute, small, harmless mood.

"""
DUBU = """Dubu design (the main character, a cream sheep):
- cream #F6F2E6 body, ONE solid color everywhere including the face. No markings, no darker face, no inner-ear color
- 2-head-tall potato body with a soft cloud-shaped fluffy outline, stubby limbs, tiny tail, two small rounded ears sticking out sideways
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes
"""
TANGJA = """Tangja design (Dubu's friend, a yellow duck, same height as Dubu):
- yellow #F5E08C body, ONE solid color everywhere including face and wings. The ONLY other color is the small flat bill and the two small webbed feet in orange #F0A83A
- 2-head-tall potato body, stubby wing arms, tiny tail tuft, a small tuft of feathers on top of the head, no neck
- face: two small black dot eyes set wide apart, a small flat orange bill instead of a nose, NO MOUTH, NO BLUSH
"""
KONG_KID = """Kong design (Dubu's little brother, a light-gray mouse, drawn here as a SMALL CHILD about 70% of Dubu's height):
- light gray #DED6DA body, ONE solid color everywhere including face and ears. No pink inner ears
- 2-head-tall potato body, stubby limbs, two BIG round ears on top of the head, one thin curly tail
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
- wears one small flat red #E53935 bow tie at the neck, nothing else
"""
CLERK = """Clerk design (a convenience-store clerk, a blue-gray seal, same height as Dubu):
- blue gray #BCD0DA body, ONE solid color everywhere. No spots
- 2-head-tall soft blob body, no neck, no ears, two short flipper arms, a small flat tail flipper at the bottom instead of legs
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH; blank empty stare
- wears a tiny plain white apron
"""
BAMTOL = """Bamtol design (Dubu's boyfriend, a warm-brown hedgehog, slightly taller than Dubu):
- warm brown #C9A582 body, ONE solid color everywhere including the face (no lighter face patch, no two-tone). The spikes are drawn ONLY as a zigzag outline around the back of the head and body; no lines or spikes drawn inside the body
- 2-head-tall rounded body, stubby limbs, small rounded ears, no tail
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
"""
APPLE = """Prop of this episode, THE APPLE: one bright green #5DBB63 apple about two thirds the size of Dubu's head, with a short brown stem and one small dark-green #2E7D32 leaf. Drawn flat and bold with the same wobbly outline, no highlight, no shading. Dubu holds it out with both hands like a gift whenever she apologizes.
"""
SILHOUETTE = "a featureless person-shaped silhouette in flat medium gray #9A9A9A, no face, no details, a plain rounded human figure a bit taller than Dubu"
LAYOUT = "Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = "\nNo text, no letters, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.\n"


def head(*designs):
    return STYLE + "".join(designs) + "\n"


cuts = {}
cuts['cover'] = head(DUBU, APPLE) + (
    "Draw ONE full-body Dubu standing on the tip of a small flat rocky ledge (a simple gray-brown rock outcrop, like Pride Rock, drawn flat), "
    "front view, feet apart, chest out, in a proud hero pose: her LEFT hand rests on her hip, and her RIGHT arm is raised diagonally up and out to the side, "
    "the arm clearly attached at the shoulder of her body (not the head), holding THE APPLE up high in that one hand like a trophy. "
    "Eyes as two small confident straight dashes. Behind her, thin light-gray radial light rays fan out from behind her body, and several small sparkles float around the apple. "
    "Character and rock in the lower 60% of the image; the upper 40% must be completely empty white for a title.") + END

cuts['cut1'] = head(DUBU, APPLE) + (
    "Scene: " + SILHOUETTE + " is walking from right to left in side view, looking straight ahead, and has just shoulder-bumped into Dubu who was standing still; "
    "it keeps walking without reacting. Dubu, on the LEFT, is knocked sideways: her body is tilted and wobbling with two short motion lines, one small black four-point impact star "
    "is drawn between the silhouette's shoulder and Dubu's shoulder — yet SHE is the one apologizing: she bends forward toward the silhouette in a deep bow, holding THE APPLE out "
    "with both hands toward it, eyes as two small dots. The two figures overlap slightly at the shoulders so the bump is obvious. Bright, calm colors. " + LAYOUT) + END

cuts['cut2'] = head(DUBU, TANGJA, APPLE) + (
    "Scene: a street (plain white background, only a thin gray ground line). Tangja (left) has just run into Dubu: she is caught mid-skid with her body leaning forward, a few short motion lines behind her, "
    "both wing arms pressed flat over her face below her eyes in shock, eyes as slightly bigger round dots. On the ground between them lies a fallen ice cream cone: a beige waffle cone tipped over with a pink scoop splatted on the ground. "
    "Dubu (right) is not upset at all: she is already bowing slightly toward Tangja, holding THE APPLE out with both hands, eyes as two closed happy upward arcs. "
    "One small heart floats above Tangja's head. Bright, warm colors. " + LAYOUT) + END

cuts['cut3'] = head(DUBU, KONG_KID, CLERK, APPLE) + (
    "Scene: inside a convenience store, years ago. Background stays plain white; only a simple flat counter on the RIGHT with the Clerk standing behind it, blank stare, flippers on the counter. "
    "On the LEFT, a metal snack shelf has toppled over sideways and a big pile of colorful snack bags (flat rectangles and pillows in red, yellow, blue, green, no letters) is spilled across the floor. "
    "Little Kong (a small child, about 70% of Dubu's height, red bow tie) stands next to the pile with both hands behind his back, head turned away pretending nothing happened, one small black music note floating above his head. "
    "Dubu, wearing a Korean high-school girl uniform (white short-sleeve shirt and a navy #2E3A59 pleated skirt), stands in the middle bending forward in a deep 90-degree bow toward the Clerk, holding THE APPLE out with both hands. "
    "Bright, warm colors. " + LAYOUT) + END

cuts['cut4'] = head(DUBU, BAMTOL, APPLE) + (
    "Scene: in front of a cafe (plain white background, only a thin gray ground line and, behind Dubu, a simple flat wooden park bench). "
    "On the bench seat sits a clear plastic cup with a straw, its drink gone pale and watery, ice fully melted, and a small puddle of condensation under it. "
    "Bamtol (left) has just arrived, strolling in slowly and unhurried, side view, arms hanging limply, eyes as two small blank dots, no sign of hurry or guilt. "
    "Dubu (right) has stood up from the bench to greet him: her body faces him, eyes as two closed happy upward arcs, one hand holding THE APPLE out toward him at chest height, "
    "while her OTHER arm is hidden behind her back and that hidden hand is clenched into a tight fist, with three short tremble lines drawn around the fist (this fist must be visible to the viewer behind her body). "
    "Colors slightly muted and desaturated. " + LAYOUT) + END

cuts['cut5'] = head(DUBU, BAMTOL) + (
    "Scene: night in a bedroom. At the bottom, Dubu lies on her back on a simple flat bed (low wooden frame, white pillow), covered up to her chest by a plain pale blue #C9D6E3 blanket with no pattern; her head, ears and both arms on top of the blanket show. "
    "Her eyes are WIDE open, drawn as two larger round black dots staring straight up, body stiff. "
    "Above her floats one large fluffy cloud-shaped thought cloud with a soft rounded outline and a very light gray fill, with NO tail and NO small trailing circles. "
    "Inside the thought cloud stands Bamtol, front view, being deliberately annoying: a pair of small flat red #E53935 devil horns on top of his head, arms crossed over his chest, head tilted back a little, eyes as two closed upward arcs (a smug, teasing look). "
    "Colors muted and dim. " + LAYOUT) + END

cuts['cut6'] = head(DUBU, APPLE) + (
    "Scene: Dubu stands in the lower middle facing the viewer, between two big push buttons, each on its own short flat gray pedestal about knee height. "
    "LEFT button: a big round bright red #E53935 button. RIGHT button: a big button shaped exactly like THE APPLE (green #5DBB63 with a stem and a leaf), the same size as the red one. "
    "Dubu's RIGHT hand is already pressed flat on top of the green apple button, pushing it down, but her head is turned toward the red button and her dot eyes look at it; one big sweat drop hangs beside her head. "
    "Keep the space directly above each button empty for labels. Colors muted and desaturated except the two buttons. " + LAYOUT) + END

cuts['cut7'] = head(DUBU, BAMTOL, APPLE) + (
    "Scene: the same cafe front as before (plain white background, a thin gray ground line, the same simple flat wooden park bench in the background, now empty). "
    "Bamtol (left) stands with his head bowed low, holding out with both hands a colorful bouquet: pink, yellow and light-blue flat flowers with green leaves wrapped in a simple beige paper cone, and ONE green APPLE (with its stem and leaf) tucked in among the flowers. "
    "Dubu (right) wears a terracotta #C77B3F hero cape knotted at the front of her neck and hanging down her back, both hands clasped together at her chest, eyes as two closed happy upward arcs. "
    "A few small flat flower petals (pink and yellow) drift in the air around them. Bright, warm colors. No sparkles. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
