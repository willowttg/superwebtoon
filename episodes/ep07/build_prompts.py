"""EP.07 프롬프트 생성. 저장소 루트에서 python episodes/ep07/build_prompts.py. 콘티는 conti.md 직접 편집."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
S = os.path.join(ROOT, "assets", "samples")


def block(name):
    """시트 프롬프트의 LINE QUALITY + design 블록."""
    t = open(os.path.join(S, f"{name}-sheet-prompt.txt"), encoding="utf-8").read()
    return t[t.index("LINE QUALITY"):t.index("\nDraw a CHARACTER")].strip() + "\n"


LINE = block("dubu").split("\n\n")[0] + "\n\n"


def design(name):
    return block(name).split("\n\n", 1)[1]


STYLE = "Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes only). Reproduce these exact character designs and this exact line quality. Cute, small, harmless mood.\n\n"
CAPE = "Dubu wears a small flat terracotta #C77B3F cape tied at the neck, hanging behind her shoulders. "
LAYOUT = " Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = "\nNo text, no letters, no numbers, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies. NO rain cloud anywhere.\n"


def head(*names):
    return STYLE + LINE + "".join(design(n) + "\n" for n in names)


cuts = {}
cuts["cover"] = head("dubu") + (
    "Camera: front view. Draw ONE full-body Dubu standing timidly: shoulders hunched up, both hands clasped together in front of her chest, "
    "knees slightly together, eyes as two small dots with her worried eyebrows, one sweat drop beside her head. " + CAPE +
    "Nothing else in the picture." + LAYOUT) + END

cuts["cut1"] = head("dubu", "halmoni") + (
    "Camera: HIGH ANGLE, looking down at a low round dining table from slightly above. "
    "Grandma deer stands on the far side of the table, leaning forward and holding out a full bowl of food with both hands toward Dubu, eyes as closed happy upward arcs, one tiny sparkle. "
    "Behind Grandma rises a tall wobbly TOWER of many more stacked bowls and plates of food (rice, soup, side dishes, fruit), taller than she is. "
    "Dubu sits on the near side of the table, seen from the front, with a hugely round bulging belly, holding a spoon in one hand; the table in front of her is crowded with half-eaten bowls. "
    "Her eyes are small dots with worried eyebrows and two thin tear streams run down from her eyes. "
    "The lineup image shows their relative sizes only. Bright warm colors." + LAYOUT) + END

cuts["cut2"] = head("dubu", "kong", "misook", "deoksu") + (
    "Camera: Dubu LARGE in the left foreground, the others small in the far background. "
    "Beach scene reduced to a few flat props: one big striped beach parasol (red and white) planted in the sand on the left, and a flat light-blue #BFE3F2 band of sea water across the far background. "
    "Dubu sits under the parasol on a small towel, in her sheep body without clothes, holding a smartphone pressed to her ear with one hand, shoulders hunched, eyes as dots with worried eyebrows and two thin tear streams. "
    "In the middle distance Kong the mouse walks toward her out of the water wearing a yellow inflatable swim ring around his waist, eyes as closed happy arcs, dripping small water drops. "
    "Far in the background, tiny, Misook the fox and Deoksu the deer float in the sea water inside swim rings, splashing, seen small. "
    "The lineup image shows their relative sizes only. Bright summer colors." + LAYOUT) + END

cuts["cut3"] = head("dubu") + (
    "Camera: LOW ANGLE from floor level, looking up. "
    "A huge messy MOUNTAIN of garish, ridiculous clothes fills the lower picture: a hot-pink feather boa, neon-green baggy pants, a leopard-print jacket, "
    "a purple sequined vest, rainbow striped socks, a zebra-striped skirt, a bright orange fur coat, all piled up and spilling sideways. "
    "Dubu sits on the very top of the pile, tiny against it, wearing a giant polka-dot hat with an oversized bow tilted crookedly on her head. "
    "Her eyes are two tired flat dashes with her worried eyebrows, arms hanging limp, staring blankly into space. "
    "Clothes in loud saturated colors, Dubu in her normal cream." + LAYOUT) + END

cuts["cut4"] = head("dubu") + (
    "Camera: SIDE VIEW, profile, Dubu running from left to right. "
    "Dubu wears a yellow hard hat (construction safety helmet) and sprints at full speed with her whole body leaning forward, arms pumping, legs a blur of motion lines, "
    "a very serious determined face: the visible eye is one squeezed-shut '>' mark with its worried eyebrow, two sweat drops flying off. "
    "She is charging straight toward a yellow folding wet-floor warning sign (a plain yellow A-frame sign with NO letters or symbols on it) standing on a shiny flat pale-blue puddle on the floor at the right. "
    "Behind her on the left stands a tall neat stack of blue and gray paper folders and documents, as tall as she is, tied with string. "
    "Flat bold colors." + LAYOUT) + END

cuts["cut5"] = head("dubu", "tangja") + (
    "Camera: 3/4 view from slightly above. "
    "Dubu is in the foreground, seen from a three-quarter front angle, holding a smartphone in both hands close to her face and tapping the screen with one thumb; "
    "her face is a displeased frown: eyes as two flat dashes, her worried eyebrows pushed down hard toward the nose, ears drooping. "
    "The phone screen shows a simple social media post: one gray rectangle image placeholder with a small outlined heart icon below it and a blank comment bar, NO letters. "
    "Right behind her, Tangja the duck leans over Dubu's shoulder from behind, both wings raised up high in excitement, big glossy highlight eyes staring at the phone, three small sparkles around her head. "
    "The lineup image shows their relative sizes only. Bright colors." + LAYOUT) + END

for n, p in cuts.items():
    with open(os.path.join(HERE, "prompts", f"{n}.txt"), "w", encoding="utf-8") as f:
        f.write(p)
print("ok", list(cuts))
