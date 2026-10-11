# -*- coding: utf-8 -*-
"""릴스 TTS — reel/script.json 의 줄마다 Qwen3-TTS CustomVoice 프리셋(sohee)으로 reel/tts/NN.wav 를 뽑고,
Whisper 로 받아 적어 일치율이 낮으면 시드를 바꿔 다시 뽑는다. 결과 길이·받아쓰기는 reel/tts/tts.json.
밥상 venv:  C:/Users/SIJIN/밥상/.venv/Scripts/python.exe scripts/reel_tts.py episodes/ep08 [줄번호 ...]
(줄번호를 주면 그 줄만 다시 뽑는다)"""
import io
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\SIJIN\밥상\기획\도구")
from qwen_tts import Qwen3TTSModel  # noqa: E402
from tts_backend import load_stt, transcribe  # noqa: E402

MODEL = r"C:\Users\SIJIN\음성모델\모델\Qwen3-TTS-12Hz-1.7B-CustomVoice"
SEEDS = [1234, 7, 42, 2026]
OK = float(os.environ.get("REEL_TTS_OK", 0.9))

ep = Path(sys.argv[1]).resolve()
redo = {int(x) for x in sys.argv[2:]}
S = json.load(open(ep / "reel/script.json", encoding="utf-8"))
out = ep / "reel/tts"
out.mkdir(parents=True, exist_ok=True)
meta_path = out / "tts.json"
meta = {m["n"]: m for m in json.load(open(meta_path, encoding="utf-8"))} if meta_path.exists() else {}


def norm(s):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", s)


def ratio(a, b):
    a, b = norm(a), norm(b)
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (ca != cb))
    return 1 - d[len(b)] / max(len(a), len(b), 1)


def trim(wav, sr, thr=0.01, pad=0.05):
    idx = np.where(np.abs(wav) > thr)[0]
    if not len(idx):
        return wav
    p = int(pad * sr)
    return wav[max(idx[0] - p, 0):idx[-1] + p]


tts = Qwen3TTSModel.from_pretrained(MODEL, device_map="cuda:0", dtype=torch.bfloat16, attn_implementation="sdpa")
stt = load_stt()
for n, L in enumerate(S["lines"], 1):
    dst = out / f"{n:02d}.wav"
    if dst.exists() and n in meta and (not redo or n not in redo):
        continue
    emo = L.get("emo", S["narr_emo"])
    best = None
    for seed in SEEDS:
        torch.manual_seed(seed)
        wavs, sr = tts.generate_custom_voice(text=L["text"], language="Korean", speaker=S["voice"], instruct=emo,
                                             max_new_tokens=int((0.5 * len(L["text"]) + 2.0) * 12.5))
        wav = trim(np.asarray(wavs[0], dtype=np.float32), sr)
        sf.write(dst, wav, sr)
        heard = transcribe(stt, str(dst))
        r = ratio(L["text"], heard)
        print(f"{n:02d} seed {seed} {len(wav) / sr:.2f}s 일치 {r:.2f}  {heard}", flush=True)
        if best is None or r > best[0]:
            best = (r, seed, wav, heard)
        if r >= OK:
            break
    r, seed, wav, heard = best
    sf.write(dst, wav, sr)
    meta[n] = dict(n=n, text=L["text"], seed=seed, dur=round(len(wav) / sr, 3), match=round(r, 2), heard=heard)
    json.dump([meta[k] for k in sorted(meta)], open(meta_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("완료")
