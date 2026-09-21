"""EP.07 A안 프롬프트 생성. python build_prompts.py (episodes/ep07 에서 실행). 콘티는 conti.md 직접 편집.
헤더 = 시트 프롬프트의 LINE QUALITY 블록 + design 블록(자동 추출)."""
import os, re

S = '../../assets/samples'


def block(name, key):
    t = open(f'{S}/{name}-sheet-prompt.txt', encoding='utf-8').read()
    m = re.search(rf'^{key}.*?(?=\n\n)', t, re.S | re.M)
    return m.group(0) + '\n\n'


LINE = block('dubu', 'LINE QUALITY')
DUBU, TANGJA, KONG = (block(n, f'{c} design') for n, c in (('dubu', 'Dubu'), ('tangja', 'Tangja'), ('kong', 'Kong')))
STYLE = ("Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes only). "
         "Reproduce these exact character designs and this exact thin pencil line quality. Flat colors, no shading, simple emotion symbols. Cute, small, harmless mood.\n\n")
MIC = ("Prop of this episode, THE MIC: a simple handheld microphone, a short mint-green #3ECFB2 handle with a round silver-gray #B0B0B0 mesh head, drawn flat and bold, no shading.\n\n")
LAYOUT = "Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = ("\nNo text, no letters, no numbers, no speech bubbles, no captions. Plain white background. "
       "One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, "
       "as a contact shadow; no other shadows, no shading on the bodies.\n")


def head(*d):
    return STYLE + LINE + ''.join(d)


cuts = {}
cuts['cut1'] = head(DUBU, MIC) + (
    "Camera: LOW ANGLE, seen from the floor in front of a small stage looking slightly up. "
    "Dubu stands alone at the center of a low flat stage (a simple pale wooden box edge is visible at the bottom), holding THE MIC with both hands right in front of her chin. "
    "Eyes as bigger glossy round eyes with a tiny white highlight (eager), worried eyebrows kept. A round pale-yellow #FFF3B0 spotlight circle on the stage floor around her feet, and several small sparkles float around her head. "
    "Bright colors. " + LAYOUT) + END

cuts['cut2'] = head(DUBU, TANGJA) + (
    "Camera: HIGH ANGLE looking almost straight down at a small bed at night. "
    "Dubu has just sat bolt upright in bed, a pale-blue blanket pushed halfway off her lap, one side of her cream wool visibly flattened and pressed flat, and one short curved crease line drawn on her cheek (pillow mark). "
    "She holds a small smartphone pressed to the side of her head with one hand. Worried eyebrows, dot eyes. "
    "Floating just above the phone is one small round inset circle with a thin outline, and inside it only Tangja's face (yellow duck, orange bill) with two tear streams running from her dot eyes. "
    "On a small nightstand beside the bed sits a small round alarm clock with a BLANK white face (no hands, no numbers). "
    "The lineup image shows their relative sizes only. Bright, soft colors. " + LAYOUT) + END

cuts['cut3'] = head(DUBU, KONG) + (
    "Camera: SIDE VIEW at an apartment entrance hall, plain white background with a thin gray floor line and a simple door frame at the far right. "
    "Kong (gray mouse) stands on the RIGHT wearing a U-shaped gray travel neck pillow around his neck, next to a big dark-blue #3F5F8F rolling suitcase as tall as himself, "
    "holding out a small car key on a ring toward Dubu with one hand, eyes as smug closed upward arcs. "
    "Dubu stands on the LEFT facing him, her head already tipped forward in a nod with two short curved motion arcs above the back of her head, worried eyebrows, dot eyes, one big sweat drop beside her head. "
    "The lineup image shows their relative sizes only. Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut4'] = head(DUBU) + (
    "Camera: EXTREME CLOSE-UP seen from just over Dubu's shoulder. Only the back of Dubu's cream head and one of her hands are visible at the bottom edge, the hand holding a smartphone upright that fills most of the lower picture; short thin tremor lines around the hand. "
    "The phone screen shows a calendar app: a plain month grid of empty white squares with thin gray lines and NO numbers; ONE square near the right column is stuffed with four colored horizontal event bars (red, blue, green, orange) stacked on top of each other and spilling out past the square's edges. All other squares are empty. "
    "Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut5'] = head(DUBU) + (
    "Camera: FRONT VIEW, evening at a bus stop, plain white background with a thin gray ground line. "
    "A simple bus stop sign pole (tall thin gray pole with a round blank sign on top) stands at the left. Dubu stands beside it facing the viewer, holding a smartphone with both hands at chest height and staring down at it, worried eyebrows, dot eyes. "
    "Behind her, farther back and smaller, a simple flat city bus in muted green is seen from its BACK, driving away, one small puff of gray exhaust behind it. "
    "The phone screen (seen from the front, small) shows a tall block of thin gray text lines at the top and one rounded gray speech-bubble shape at the bottom, both BLANK. "
    "One small black scribbled swirl floats above her head. Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut6'] = head(DUBU, TANGJA, MIC) + (
    "Camera: SIDE VIEW, daytime street, plain white background with only a thin gray ground line. Both characters walk from left to right. "
    "Dubu wears a terracotta #C77B3F hero cape knotted at the front of her neck and flowing behind her, THE MIC held down at her side in one hand, eyes as two closed happy upward arcs, worried eyebrows kept. "
    "Tangja walks right beside her, clinging to Dubu's other arm with both wings, leaning her head toward Dubu, eyes as bigger glossy round eyes with highlights. "
    "A few small black five-point stars float in the air around them (no sparkles). The lineup image shows their relative sizes only. Bright, warm colors. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
