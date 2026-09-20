"""EP.03 프롬프트 생성. python build_prompts.py (episodes/ep03 에서 실행). 콘티는 conti.md."""
HEADER = """Reference images:
- The FIRST image is the CHARACTER SHEET of Dubu, a cream-colored sheep. Reproduce this exact character design.
- Further character sheets / a size lineup may follow; the lineup image shows their relative sizes.
- The last two images are STYLE references only (the Korean instatoon dog "Kkamja"): copy its drawing grammar — wobbly hand-drawn black outline of uneven thickness, flat colors, no shading, simple emotion symbols (sweat drop, sparkles, tiny rain cloud, hearts) — but NOT its character or color.

Dubu design:
- cream #F6F2E6 body, ONE solid color everywhere including the face. No markings, no darker face, no inner-ear color
- 2-head-tall potato body with a soft cloud-shaped fluffy outline, stubby limbs, tiny tail, two small rounded ears sticking out sideways
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes

Prop of this episode, THE BLANKET: a soft cobalt blue #3F6FE0 blanket scattered with small flat yellow #FFD23F five-point stars. Drawn flat, bold, simple, with the same wobbly outline. When Dubu WEARS it as a cape, it is knotted at the front of her neck and hangs down her back, flowing behind her.

"""
END = ("\nNo text, no letters, no speech bubbles, no captions. Plain white background. "
       "One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object "
       "resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.\n")
END_NOSHADOW = "\nNo text, no letters, no speech bubbles, no captions. Plain white background. No shadows at all, no shading on the bodies.\n"

TANGJA = "- Tangja, a yellow #F5E08C duck: ONE solid color, flat orange #F0A83A bill and webbed feet, stubby wing arms, small feather tuft on top of the head, dot eyes, no mouth. Same height as Dubu."
SORA = "- Sora, a slate gray #C2C6CA penguin: ONE solid color including the belly, tiny yellow #E8B24A beak and feet, short flipper arms, no ears, dot eyes, no mouth. Same height as Dubu."
KONG = "- Kong, a light gray #DED6DA mouse: ONE solid color, two BIG round ears on top of the head, one thin curly tail, dot eyes, no mouth. Same height as Dubu."
CATS = "- Three cats (see the cats sheet): identical design, small pointed triangular ears in the same flat color as the body, thin short tail, dot eyes, no mouth. Pink #F2C9CF, lavender #D6CBE6, mint #C5DCCB. Same height as Dubu."

cuts = {}
cuts['cover'] = ("Draw ONE full-body Dubu, front view, wearing THE BLANKET as a cape, in a hero pose: feet apart, chest out, "
    "one hand on her hip, the other arm raised straight up holding a smartphone high in the air. Behind her, thin light-gray "
    "radiating lines fan out from her body like a halo burst. A few small sparkles around her. Character in the lower 60% of the image, "
    "the upper 40% must be completely empty white for a title." + END)

cuts['cut1'] = ("Upper-body portrait of Dubu, from the waist up, front view, drawn large. She wears a black suit jacket over a white "
    "dress shirt with the top button open and no tie (the jacket and shirt are drawn flat and simple with the same wobbly outline; "
    "her cream head, ears and hands stay uncovered). She raises one index finger straight up beside her head, like someone stating a "
    "life motto with quiet confidence. Her eyes are two small closed downward-curving arcs - relaxed, smug, half-lidded - and she has "
    "no mouth as always. Her other hand holds a smartphone out toward the viewer so its screen is fully visible: a simple messenger "
    "chat UI, a thin header bar with one small circle avatar, and ONE white rounded chat bubble aligned to the left, completely empty "
    "inside. No sparkles, no emotion symbols. The figure is cut off at the waist, so there is no ground and no shadow in this picture. "
    "Figure in the lower 60% of the image, the upper 40% completely empty white." + END_NOSHADOW)

cuts['cut2'] = ("Additional character (see her sheet):\n" + TANGJA + "\n"
    "Over-the-shoulder view from behind Tangja. In the lower left foreground, the BACK of Tangja's head and shoulders are drawn large: "
    "only the back of her round yellow head with the feather tuft standing stiffly straight up in alarm - no face, no eyes. "
    "One sweat drop flies off the side of her head. She holds a smartphone up in front of her to the right so that its screen is fully "
    "visible to the viewer over her shoulder: a dark rounded rectangle, on its screen a simple messenger chat UI with a thin header bar "
    "with one small circle avatar, and ONE large white rounded chat bubble aligned to the left, completely empty inside, with one small "
    "flat red heart sitting at the bubble's lower corner. From the top of Tangja's head, a chain of three small circles rises up and to "
    "the right into ONE big fluffy white thought cloud with a black outline. INSIDE the thought cloud: Dubu as a serene Buddha - sitting "
    "cross-legged on a flat pink lotus pedestal, THE BLANKET draped over one shoulder and across her body like a monk's robe, both stubby "
    "hands pressed together in prayer at her chest, eyes as two small closed downward arcs, and a flat golden circular halo disc behind "
    "her head. Layout: the upper 35% of the image is completely empty white; the thought cloud sits below that line in the upper-middle "
    "right; the phone is on the right at mid height; the back of Tangja's head fills the lower left." + END_NOSHADOW)

cuts['cut3'] = ("Additional characters (see the sheets and the lineup):\n" + SORA + "\n" + CATS + "\n"
    "Scene: a house party. In the background on the right, the three cats dance excitedly among five floating balloons on strings "
    "(flat red, yellow, blue, pink, green), eyes as closed upward arcs, arms raised, small motion lines. In the foreground on the left, "
    "Dubu (no cape, no props) sneaks away on tiptoe toward a simple flat brown door frame at the left edge, one arm wrapped around Sora "
    "to support her. Sora is completely drained: body slumped, flippers hanging, eyes as two small half-closed dashes, three short "
    "vertical gloom lines on her forehead, feet dragging. Dubu glances back over her shoulder at the party with dot eyes. "
    "All characters full body, in the lower 60% of the image; the upper 40% empty white." + END)

cuts['cut4'] = ("Additional character (see her sheet and the lineup):\n" + TANGJA + "\n"
    "Scene: a classic Western gunfight standoff in a desert, drawn in muted desaturated sepia tones (dusty beige ground line, everything "
    "else low-saturation brown and gray; the characters keep their own body colors but slightly dulled). Dubu stands at the far LEFT and "
    "Tangja at the far RIGHT, both in side view facing each other across the width of the picture. Each wears a flat brown cowboy hat, "
    "a brown leather vest and a gun belt with a holster on the hip, and each has one hand hovering tensely just above the pistol grip, "
    "fingers spread. Both stand stiff and still, eyes as small dots. Between them on the ground, one round dry tumbleweed. A single thin "
    "jagged lightning-shaped line is drawn in the air between their eyes to show the tension. Both characters full body, in the lower "
    "55% of the image; the upper 45% empty white." + END)

cuts['cut5'] = ("Additional character (see his sheet and the lineup):\n" + KONG + "\n"
    "Scene: the same desert, same muted sepia tones. Dubu lies flat on her back on the ground in the lower middle, having lost the duel, "
    "but she is blissfully happy: eyes as two closed upward arcs. She is tucked in up to the chest under THE BLANKET (its cobalt blue and "
    "yellow stars are the ONLY saturated colors in the picture), her cowboy hat lies fallen beside her head, and there is one small flat "
    "red dot on her chest just above the blanket's edge. Kong stands to the right of her, also in a brown cowboy hat, brown vest and gun "
    "belt, looking down at her with dot eyes and his head tilted, one black question mark floating above his head. Full bodies, in the "
    "lower 55% of the image; the upper 45% empty white." + END)

cuts['cut6'] = ("Additional character (see his sheet and the lineup):\n" + KONG + "\n"
    "Scene: an old, rusty Korean two-wheeled hand tractor (a walking tractor / power tiller), side view, drawn flat and simple: a boxy gray "
    "engine block with rust patches, two big red wheels with gray hubs, long handlebars sticking back, and a thin upright exhaust pipe. "
    "Mounted on the FRONT face of the engine block, in place of the engine cover, is Dubu's sleeping face: her round cream cloud-shaped "
    "head with two little ears, eyes as two small closed downward arcs, dot nose, no mouth, peacefully asleep, with a small sleep symbol "
    "of three ascending z-shapes drawn as simple strokes above it. In front of the tractor, Kong grips a hand crank starting handle "
    "inserted into the engine with both hands, his whole body straining backward, feet planted wide, motion lines around the crank and a "
    "few sweat drops off his head. Thick puffs of black smoke rise from the exhaust pipe. Muted, slightly desaturated colors. Everything "
    "in the lower 60% of the image; the upper 40% empty white." + END)

cuts['cut7'] = ("Additional characters (see the sheets and the lineup):\n" + TANGJA + "\n" + SORA + "\n"
    "Scene: a simple pub table. In the lower left, a flat brown square table with two full beer mugs on it. Tangja and Sora sit on the "
    "far side of the table facing right, both with arms flung wide open in welcome and eyes as closed upward arcs, one small heart "
    "floating above each of their heads. From the upper right, Dubu FLIES in like a superhero arriving late: her body horizontal in the "
    "air, one arm stretched straight forward, the other tucked back, THE BLANKET streaming behind her as a cape, several long horizontal "
    "speed lines trailing behind her. Bright, warm colors. Dubu is in mid-air, so NO shadow under her; contact shadows only under the "
    "table and the seated characters. Everything in the lower 60% of the image; the upper 40% empty white." + END)

import os
os.makedirs('prompts', exist_ok=True)
open('prompts/_header.txt', 'w', encoding='utf-8', newline='\n').write(HEADER)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(HEADER + v)
print(sorted(os.listdir('prompts')))
