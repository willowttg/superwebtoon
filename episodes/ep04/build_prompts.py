"""EP.04 프롬프트 생성. python build_prompts.py (episodes/ep04 에서 실행). 콘티는 conti.md 직접 편집."""
import os

STYLE = """Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes). Reproduce these exact character designs. Drawing grammar: wobbly hand-drawn black outline of uneven thickness, flat colors, no shading, simple emotion symbols. Cute, small, harmless mood.

"""
DUBU = """Dubu design (the main character, a cream sheep):
- cream #F6F2E6 body, ONE solid color everywhere including the face. No markings, no darker face, no inner-ear color
- 2-head-tall potato body with a soft cloud-shaped fluffy outline, stubby limbs, tiny tail, two small rounded ears sticking out sideways
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH, no eyelashes
"""
MISOOK = """Misook design (Dubu's mother, a soft-orange fox, slightly taller than Dubu):
- soft orange #F6CA9E body, ONE solid color everywhere including face, ears, tail. No white chest, no dark ear tips
- 2-head-tall potato body, stubby limbs, large pointed triangular ears, one big bushy tail curling up beside the body
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
"""
DEOKSU = """Deoksu design (Dubu's father, a tan deer, the tallest):
- tan #EACEAA body, ONE solid color everywhere including face and ears. No spots, no white belly
- 2-head-tall potato body, stubby limbs, tiny tail, small upright ears, a pair of SIMPLE TWO-PRONG antlers (one stem with one short branch each) in a darker brown exactly as in his sheet
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
"""
KONG = """Kong design (Dubu's little brother, a light-gray mouse, same height as Dubu):
- light gray #DED6DA body, ONE solid color everywhere including face and ears. No pink inner ears
- 2-head-tall potato body, stubby limbs, two BIG round ears on top of the head, one thin curly tail
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH
"""
CLERK = """Clerk design (a restaurant waiter, a blue-gray seal, same height as Dubu):
- blue gray #BCD0DA body, ONE solid color everywhere. No spots
- 2-head-tall soft blob body, no neck, no ears, two short flipper arms, a small flat tail flipper at the bottom instead of legs
- face: two small black dot eyes set wide apart, one small dark dot nose, NO MOUTH, NO BLUSH; blank empty stare
- wears a tiny plain white apron
"""
WATCH = """Prop of this episode, THE POCKET WATCH: a round pocket watch about half the size of Dubu's head, hanging on a thin black chain around Dubu's neck so it rests on her chest. Hot pink #E64980 case with its lid flipped open, a mint #5EDBB5 dial with two simple black hands and no numbers. Drawn flat and bold with the same wobbly outline.
"""
TABLE = "Setting: a family restaurant, but the background stays plain white — only a simple flat light-wood rectangular dining table seen from the front, with the characters seated behind it on simple stools so their upper bodies show above the table top. A few tiny flat props on the table: a water pitcher, small side-dish plates, cups. "
MENU = "The MENU is a folded booklet with blank pages — only faint light-gray horizontal lines and a few small pale colored rectangles as photo placeholders, no letters at all. "
FROZEN = "FROZEN characters are drawn entirely in ONE flat pale blue-gray #D5DBE1 (their body color, props and everything they hold become that same gray, black outline kept), stiff, caught mid-motion, with a small black pause symbol (two short vertical bars) floating above each frozen head. "
LAYOUT = "Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = "\nNo text, no letters, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.\n"


def head(*designs):
    return STYLE + "".join(designs) + "\n"


cuts = {}
cuts['cover'] = head(DUBU, WATCH) + (
    "Draw ONE full-body Dubu, front view, wearing THE POCKET WATCH, striking the famous DIO 'The World' time-stop pose from JoJo: "
    "upper body leaned back dramatically, one arm thrust forward toward the viewer with the hand wide open, palm out, fingers spread, "
    "the other hand on her hip, feet apart, chin up, eyes as two small confident straight dashes. Several small sparkles around her. "
    "Behind her, a little to one side, stands a simple A-frame sidewalk sign (a chalkboard easel sign, dark green board, wooden frame) that is completely blank. "
    "Character in the lower 60% of the image; the upper 40% must be completely empty white for a title.") + END

cuts['cut1'] = head(DUBU, MISOOK, DEOKSU, KONG, CLERK, WATCH) + TABLE + MENU + FROZEN + (
    "Scene: the moment Dubu opens the menu, the whole world freezes. Seated behind the table from left to right: Misook, Deoksu, Dubu, Kong. "
    "Dubu is the ONLY one in full color: she wears THE POCKET WATCH and holds the open MENU up with both hands, dot eyes on it, calm. "
    "Everyone else is FROZEN gray: Misook tilting a cup so that a blob of water hangs suspended in mid-air between the cup and the table; "
    "Deoksu holding a half-unfolded wet towel; Kong with chopsticks lifting a side dish halfway to his face; and the Clerk standing at the right end of the table "
    "with a small notepad and a pen raised, caught mid-word. Pause symbols above the four frozen heads. " + LAYOUT) + END

cuts['cut2'] = head(DUBU, MISOOK) + TABLE + MENU + (
    "Scene: only Dubu and Misook, seated side by side behind the table. Dubu (right) has flipped the MENU to its very last page and holds it so close that it almost touches her nose, "
    "reading the tiny corner of the page; her dot eyes point at the bottom corner of the page. Misook (left) leans her whole body sideways toward Dubu to peek at the same corner, "
    "eyes as slightly bigger round dots, one small heart floating above Misook's head. Bright, warm colors. Keep the lower-right corner of the menu page plain and visible so a label can be added later. " + LAYOUT) + END

cuts['cut3'] = head(DUBU, DEOKSU) + TABLE + (
    "Scene: only Dubu and Deoksu, seated side by side behind the table. Between them a MENU page is propped up, showing one big flat picture of a bright red spicy stew in a black bowl, "
    "and below it several faint gray lines, the last line at the very bottom being the item Dubu points at with one stubby finger (no letters anywhere). "
    "Deoksu (left) sits very straight with his arms crossed, pretending to be fine, eyes as two small straight dashes, but ONE sweat drop slides down his forehead. "
    "Dubu (right) turns toward him, eyes as closed happy upward arcs, pointing at the bottom of the menu. Bright, warm colors. " + LAYOUT) + END

cuts['cut4'] = head(DUBU, MISOOK, DEOKSU, KONG, CLERK, WATCH) + TABLE + MENU + FROZEN + (
    "Scene: the same table as before, but reversed — now DUBU is the only FROZEN one. Seated behind the table from left to right: Misook, Deoksu, Dubu, Kong. "
    "Dubu is entirely flat gray #D5DBE1 (body, pocket watch and the menu she holds), stiff, holding the open MENU in front of her with dot eyes on the first page, "
    "and a thin cobweb (a few simple radial lines with rings) is spun between the top of the menu and her head. No pause symbol on her. "
    "Everyone else is in normal full color and busy: the Clerk stands at the LEFT end of the table, turned toward Misook, writing on the notepad; Misook points at her own menu ordering; "
    "Deoksu drinks from a cup; Kong already eats a side dish with chopsticks, eyes as closed happy arcs, a couple of small motion lines near his chopsticks. "
    "Colors slightly muted. " + LAYOUT) + END

cuts['cut5'] = head(DUBU, MISOOK, DEOKSU, KONG) + TABLE + MENU + (
    "Scene: seated behind the table from left to right: Misook, Deoksu, Dubu, Kong. Misook, Deoksu and Kong all clutch their bellies with both hands and cry: "
    "dot eyes with two thin tear streams each, shoulders hunched, drooping. Dubu ignores them completely and studies the MENU like a textbook: "
    "she wears small round black-rimmed glasses, holds a yellow highlighter pen and is drawing a bright yellow line across one menu line, several small colored sticky notes (pink, yellow, blue) stick out of the menu's edges, "
    "and an open notebook with a pencil lies on the table beside her. Colors muted. Keep a little space beside each crying belly for small labels. " + LAYOUT) + END

cuts['cut6'] = head(DUBU, KONG) + TABLE + (
    "Scene: only Dubu and Kong, seated side by side behind the table, the food has arrived. In front of Dubu (left): a bowl of jajangmyeon — noodles with flat dark-brown black-bean sauce and a few cucumber slivers. "
    "In front of Kong (right): a bowl of jjamppong — bright red spicy soup with noodles and a few small seafood bits. Kong eats happily, chopsticks up, eyes as closed upward arcs. "
    "Dubu holds her chopsticks over her own bowl but her head is turned sideways toward Kong's red bowl, dot eyes fixed on it, and three short vertical gloom lines are drawn on her forehead. "
    "Colors muted except the two bowls. " + LAYOUT) + END

cuts['cut7'] = head(DUBU, MISOOK, DEOKSU, KONG, WATCH) + TABLE + MENU + (
    "Scene: seated behind the table, Dubu in the CENTER facing the viewer, Misook and Deoksu on her left, Kong on her right. "
    "Dubu wears THE POCKET WATCH and a terracotta #C77B3F hero cape tied at her neck (the cape spreads behind her shoulders), and holds the MENU spread wide open with both hands, chest out, "
    "eyes as two small determined straight dashes, looking straight at the viewer; a small white glint on the watch lid. "
    "Misook, Deoksu and Kong all rest their chins on one hand, relaxed and patient, eyes as closed upward arcs, no hurry. Bright, warm colors. No sparkles. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
