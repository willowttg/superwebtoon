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
WATCH = """Prop of this episode, THE POCKET WATCH: a round pocket watch about half the size of Dubu's head, hanging on a thin black chain around Dubu's neck so it rests on her chest. Bright red #E53935 case with its lid flipped open, a blue #3A7BD5 dial with two simple black hands and no numbers. Drawn flat and bold with the same wobbly outline.
"""
TABLE = "Setting: a family restaurant, but the background stays plain white — only a simple flat light-wood rectangular dining table seen from the front, with the characters seated behind it on simple stools so their upper bodies show above the table top. A few tiny flat props on the table: a water pitcher, small side-dish plates, cups. "
MENU = "The MENU is a folded booklet with blank pages — only faint light-gray horizontal lines and a few small pale colored rectangles as photo placeholders, no letters at all. "
FROZEN = "FROZEN characters are drawn entirely in ONE flat pale blue-gray #D5DBE1 (their body color, props and everything they hold become that same gray, black outline kept), stiff, caught mid-motion, with a small black pause symbol (two short vertical bars) floating above each frozen head. "
CAMERA_NOTE = "If a size lineup image is given it is only for the characters' relative sizes, not for the seating layout or camera. "
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

cuts['cut1'] = head(DUBU, MISOOK, DEOKSU, KONG, CLERK, WATCH) + CAMERA_NOTE + (
    "CAMERA: high angle, looking down at the dining table from above and slightly in front, so the table top is a large light-wood rectangle in the middle of the picture and the four seated characters are seen from above around it, each on a small stool (Misook and Deoksu on the far side, Dubu and Kong on the near side, Dubu at the front-right); the Clerk stands beside the table at the right. Plain white background around the table. "
    + MENU + FROZEN +
    "Scene: the moment Dubu opens the menu, the whole world freezes. Dubu is the ONLY one in full color: she wears THE POCKET WATCH and holds the open MENU up with both hands, calm. "
    "Everyone else is FROZEN gray: Misook tilting a cup so that a blob of water hangs suspended in mid-air above the table; Deoksu holding a half-unfolded wet towel; "
    "Kong with chopsticks lifting a side dish halfway to his face; the Clerk holding a small notepad and a pen, caught mid-word. Pause symbols above the four frozen heads. "
    "On the table: a water pitcher, cups, small side-dish plates. Everything in the lower 65% of the image; the upper 35% must be completely empty white.") + END

cuts['cut2'] = head(DUBU, MISOOK) + CAMERA_NOTE + MENU + (
    "CAMERA: extreme close-up. The bottom corner of the MENU's last page fills the lower-left half of the picture at an angle, held by Dubu's two stubby cream hands; Dubu's face is partly visible right behind the page, very close, her dot eyes aimed at the page corner. "
    "From the right edge, Misook's face and one big pointed ear lean into the frame, close to Dubu's, peeking at the same corner, eyes as slightly bigger round dots, one small heart floating above her head. "
    "Both are seated at a table (only the table edge shows at the very bottom); no full bodies. Keep the visible corner of the menu page plain so a label can be added later. Bright, warm colors. "
    "Everything in the lower 65% of the image; the upper 35% must be completely empty white.") + END

cuts['cut3'] = head(DUBU, DEOKSU) + CAMERA_NOTE + (
    "CAMERA: side view, full profile, the camera at table height looking along the table from its end. Deoksu and Dubu sit side by side on stools, both in profile facing left, Deoksu nearer to the camera and Dubu just behind him, the table edge running across the lower part of the picture. "
    "Scene: a MENU page is propped up on the table in front of them, seen edge-on at a slight angle so its picture is still visible: one big flat picture of a bright red spicy stew in a black bowl, and faint gray lines below it. "
    "Deoksu sits very straight with his arms crossed, pretending to be fine, eye as a small straight dash, ONE sweat drop sliding down his forehead. Dubu leans forward past him, eyes as closed happy arcs, pointing with one stubby finger at the very bottom line of the menu. "
    "A water pitcher and two cups on the table. Bright, warm colors. " + LAYOUT) + END

cuts['cut4'] = head(DUBU, MISOOK, DEOKSU, KONG, CLERK, WATCH) + CAMERA_NOTE + MENU + FROZEN + (
    "CAMERA: Dubu large in the foreground, the others small in the back. In the lower-right foreground, seen from behind at a three-quarter angle over her shoulder, Dubu sits on a stool and is drawn BIG: the back of her fluffy head, one ear, her shoulders, the pocket watch chain at her neck and the open MENU she holds up — all of it FROZEN flat gray #D5DBE1, stiff, with a thin cobweb (simple radial lines with rings) spun between the top of the menu and her head. No pause symbol on her. "
    "Beyond her, smaller and farther away across the table, in normal full color and busy: Misook seated pointing at her own menu while the Clerk STANDS on the floor beside the table next to her (the Clerk is a waiter, never seated, no stool under him) writing on a notepad, Deoksu seated drinking from a cup, Kong seated eating a side dish with chopsticks, eyes as closed happy arcs, small motion lines near his chopsticks. All seated characters on stools. "
    "Colors slightly muted. " + LAYOUT) + END

cuts['cut5'] = head(DUBU, MISOOK, DEOKSU, KONG) + TABLE + MENU + (
    "Scene: seated behind the table from left to right: Misook, Deoksu, Dubu, Kong. Misook, Deoksu and Kong all clutch their bellies with both hands and cry: "
    "dot eyes with two thin tear streams each, shoulders hunched, drooping. Dubu ignores them completely and studies the MENU like a textbook: "
    "she wears small round black-rimmed glasses, holds a yellow highlighter pen and is drawing a bright yellow line across one menu line, several small colored sticky notes (pink, yellow, blue) stick out of the menu's edges, "
    "and an open notebook with a pencil lies on the table beside her. Colors muted. Keep a little space beside each crying belly for small labels. " + LAYOUT) + END

cuts['cut6'] = head(DUBU, KONG) + CAMERA_NOTE + (
    "CAMERA: low angle from table-top level, the bowls large in the foreground. At the very front, drawn big and close: on the left a bowl of jajangmyeon (noodles under flat dark-brown black-bean sauce with a few cucumber slivers), on the right a bowl of jjamppong (bright red spicy soup with noodles and small seafood bits), both seen from just above their rims. "
    "Behind the bowls, smaller, Dubu and Kong sit side by side on stools: Kong (right) eats happily with chopsticks lifting noodles, eyes as closed upward arcs. Dubu (left) holds her chopsticks limply over her own bowl, but her whole head is turned to the right toward Kong's red bowl, both dot eyes shifted to the corners staring at it (side-eye), three short vertical gloom lines on her forehead. "
    "Colors muted except the two bowls. No sparkle or emphasis lines. " + LAYOUT) + END

cuts['cut7'] = head(DUBU, MISOOK, DEOKSU, KONG, WATCH) + TABLE + MENU + (
    "Scene: seated behind the table, Dubu in the CENTER facing the viewer, Misook and Deoksu on her left, Kong on her right. "
    "Dubu wears THE POCKET WATCH and a terracotta #C77B3F hero cape tied at her neck (the cape spreads behind her shoulders), and holds the MENU spread wide open with both hands, chest out, "
    "eyes as two small determined straight dashes, looking straight at the viewer; a small white glint on the watch lid. "
    "Misook, Deoksu and Kong all rest their chins on one hand, relaxed and patient, eyes as closed upward arcs, no hurry. Bright, warm colors. No sparkles. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
