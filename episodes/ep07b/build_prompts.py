"""EP.07 B안(대사 전용) 프롬프트 생성. python build_prompts.py (episodes/ep07b 에서 실행). 콘티는 conti.md 직접 편집.
헤더 = 시트 프롬프트의 LINE QUALITY 블록 + design 블록(자동 추출)."""
import os, re

S = '../../assets/samples'


def block(name, key):
    t = open(f'{S}/{name}-sheet-prompt.txt', encoding='utf-8').read()
    m = re.search(rf'^{key}.*?(?=\n\n)', t, re.S | re.M)
    return m.group(0) + '\n\n'


LINE = block('dubu', 'LINE QUALITY')
DUBU, TANGJA, SORA, MISOOK, KONG, BAMTOL = (block(n, f'{c} design') for n, c in (
    ('dubu', 'Dubu'), ('tangja', 'Tangja'), ('sora', 'Sora'), ('misook', 'Misook'), ('kong', 'Kong'), ('bamtol', 'Bamtol')))
STYLE = ("Reference images are CHARACTER SHEETS (and, if present, a size lineup image which shows the characters' relative sizes only). "
         "Reproduce these exact character designs and this exact thin pencil line quality. Flat colors, no shading, simple emotion symbols. Cute, small, harmless mood.\n\n")
MIC = ("Prop of this episode, THE MIC: a simple handheld microphone, a short mint-green #3ECFB2 handle with a round silver-gray #B0B0B0 mesh head, drawn flat and bold, no shading.\n\n")
GLOVES = "a pair of red #E53935 rubber kitchen gloves"
TICKETS = "two small rectangular concert tickets (plain pale-pink cards with a perforated stub line, blank)"
STICK = "a small concert light stick (a short white handle with a round glowing pale-pink #FFC1D9 tip)"
LAYOUT = "Everything in the lower 60% of the image; the upper 40% must be completely empty white."
END = ("\nNo text, no letters, no numbers, no speech bubbles, no captions. Plain white background. "
       "One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, "
       "as a contact shadow; no other shadows, no shading on the bodies.\n")


def head(*d):
    return STYLE + LINE + ''.join(d)


cuts = {}
cuts['cut1'] = head(DUBU, TANGJA, MIC) + (
    "Camera: FRONT VIEW. Dubu stands at the center holding THE MIC with one hand right in front of her chin like a singer, standing very straight and serious, worried eyebrows, dot eyes. "
    "Tangja stands right beside her on the right, leaning her whole body toward Dubu and cupping one wing beside her own head as if listening closely, eyes as bigger glossy round eyes with highlights. "
    "Several small sparkles float around Dubu's head. The lineup image shows their relative sizes only. Bright colors. " + LAYOUT) + END

cuts['cut2'] = head(DUBU, SORA, MIC) + (
    "Camera: seen from BEHIND Dubu, 3/4 over her shoulder. The back of Dubu's cream head and one shoulder are in the LEFT foreground, large; her arm on that side holds THE MIC down low. Her other arm is bent behind her back with the hand clenched into a tight fist. "
    "Facing her, a little farther away, stands Sora (gray penguin) holding " + TICKETS + " pressed against her chest with both flippers and pushing them slightly forward, head tipped down a little, downcast dot eyes. "
    "One small heart floats above Sora's head. The lineup image shows their relative sizes only. Bright, soft colors. " + LAYOUT) + END

cuts['cut3'] = head(DUBU, MISOOK) + (
    "Camera: SIDE VIEW, plain white background with a thin gray floor line. "
    "Misook (orange fox) is on the LEFT, already walking away toward the left edge, not looking back, one arm stretched straight back behind her holding out " + GLOVES + ". "
    "Dubu is on the RIGHT: one hand pressed to the front of her own throat, the other hand reaching out to take the gloves, but her two feet point to the RIGHT, away from Misook. Worried eyebrows, dot eyes, one big sweat drop beside her head. "
    "The lineup image shows their relative sizes only. Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut4'] = head(DUBU, KONG) + (
    "Camera: from BEHIND Dubu, who faces a tall rectangular wall mirror with a thin frame. Dubu's back is in the foreground; in the mirror we see her face: worried eyebrows, dot eyes, one hand placed flat on her chest in a practicing posture. "
    "Three small blank yellow sticky notes are stuck on the mirror frame. "
    "At the RIGHT edge of the picture a door stands ajar, and Kong (gray mouse) pokes only his head and one open hand through the gap, eyes as smug closed upward arcs. "
    "Dubu's other arm is already stretched out toward Kong holding a single flat banknote (a plain pale-green rectangle, blank). One small black scribbled swirl floats above Dubu's head. "
    "The lineup image shows their relative sizes only. Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut5'] = head(DUBU, BAMTOL) + (
    "Camera: HIGH ANGLE looking down at a room floor. Dubu lies flat on her back on the floor, arms and legs spread out. On the floor beside her lie " + GLOVES + " (taken off), " + TICKETS + ", and a small open wallet that is empty. "
    "Bamtol (brown hedgehog with round glasses) stands next to her, holding a smartphone in one hand and looking down at her. "
    "Dubu, still lying down, raises one bare hand with the palm pushed firmly toward Bamtol (a stop gesture). Three short thin vertical gloom lines are drawn on Dubu's forehead. "
    "The lineup image shows their relative sizes only. Contact-shadow ellipse under Dubu's lying body as well. Colors muted and low-saturation. " + LAYOUT) + END

cuts['cut6'] = head(DUBU, SORA, MIC) + (
    "Camera: SIDE VIEW, night, plain white background with only a thin gray ground line. Both characters walk from left to right. "
    "Dubu wears a terracotta #C77B3F hero cape knotted at the front of her neck and flowing behind her, THE MIC in one hand and " + STICK + " in the other, eyes as two closed happy upward arcs, worried eyebrows kept. "
    "Sora walks beside her holding " + STICK + " in one flipper, turning her head toward Dubu, eyes as small closed upward arcs. "
    "A few small black five-point stars float in the air above them (no sparkles). The lineup image shows their relative sizes only. Bright, warm colors. " + LAYOUT) + END

os.makedirs('prompts', exist_ok=True)
for k, v in cuts.items():
    open(f'prompts/{k}.txt', 'w', encoding='utf-8', newline='\n').write(v)
print(sorted(os.listdir('prompts')))
