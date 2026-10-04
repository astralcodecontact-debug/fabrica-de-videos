---
name: mindforge-quote-intro
description: "Create a MindForge Studio video intro: a real, attributed quote as an animated card (italic serif on white, words fading in word by word, author in spaced caps), exported as a 1080p MP4. Use whenever Capitao asks for an intro, opening, or quote card for the MindForge channel."
---

# MindForge quote intro

Capitao opens every MindForge Studio video with a motivational quote card. When he asks for an intro, an opening, or a quote card for that channel, produce a short animated MP4 in the locked style below and deliver it with SendUserFile.

## The locked style (do not drift from this)

- Format: 1920x1080, 30fps, about 4 to 5 seconds, H.264 MP4 (`yuv420p`, `+faststart`).
- Background: plain pure white `#ffffff`. Text: warm near-black `#181614` (not pure black).
- Quote: elegant serif in ITALIC (Lora Italic), sentence case (keep the quote's real casing, never all caps), wrapped in real curly quotes `“ ”`.
- Size: small, with generous whitespace. Narrow column (~860px max width), auto-fit font so it never fills the frame.
- Author: upright, UPPERCASE, letter-spaced, same ink color as the quote, smaller, centered under a thin short rule.
- Animation: the quote reveals word by word, each word fading in with a subtle upward rise (staggered). The author reveals last, after the whole quote. Everything fades out together at the end.

## Quote sourcing (non-negotiable)

- Use REAL quotes actually said or written by a real person, with the correct attribution. Never invent a quote and never guess who said it. A lot of popular "quotes" online are misattributed, so verify before rendering; if unsure of the source, pick a different one you are sure of, or web-search to confirm.
- Default lane is Stoic philosophers (Marcus Aurelius, Seneca, Epictetus). Other lanes on request: athletes and champions (Kobe Bryant, Muhammad Ali, Michael Jordan, David Goggins), entrepreneurs and builders. Keep the theme discipline, focus, grind, mindset.
- Translations from Greek or Latin vary; use a standard faithful English rendering and do not present it as the single exact wording.
- One clip per quote. If he asks for a batch, render several and deliver them together.

## How to build it

1. Pick or confirm the quote(s) and author(s), verified per the rules above.
2. Write the script below to the working directory (or scratchpad) as `mindforge_intro.py`.
3. Run it once per quote: `python3 mindforge_intro.py "<quote>" <out.mp4> "<Author>"`.
4. Deliver every MP4 with SendUserFile (display render). Do not paste internal paths in chat.

Environment needs `ffmpeg` and Python `Pillow`, both normally present. Fonts: Lora variable at `/usr/share/fonts/truetype/google-fonts/` (the script falls back to DejaVu Serif if missing, but Lora is the intended look; install or locate a Lora/quality serif if the fallback triggers).

## The generator script

```python
import sys, os, tempfile, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

QUOTE  = sys.argv[1]
OUT    = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "intro.mp4")
AUTHOR = sys.argv[3] if len(sys.argv) > 3 else ""

W, H, FPS = 1920, 1080, 30
INK, BG = (24, 22, 20), (255, 255, 255)

def fonts():
    it = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
    up = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
    if not os.path.exists(it):
        it = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
        up = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    return it, up
F_ITAL, F_UP = fonts()

def load(path, size, variation=None):
    f = ImageFont.truetype(path, size)
    if variation:
        try: f.set_variation_by_name(variation)
        except Exception: pass
    return f

DISP = "“" + QUOTE.strip() + "”"
tmp = tempfile.mkdtemp(); fd = os.path.join(tmp, "frames"); os.makedirs(fd)
probe = ImageDraw.Draw(Image.new("RGB", (4, 4)))
def wlen(t, f): return probe.textlength(t, font=f)

def wrap(words, font, maxw):
    lines, cur = [], []
    for w in words:
        if wlen(" ".join(cur + [w]), font) <= maxw or not cur: cur.append(w)
        else: lines.append(cur); cur = [w]
    if cur: lines.append(cur)
    return lines

maxw = 860
for size in range(72, 32, -3):
    fontQ = load(F_ITAL, size, "Medium Italic")
    lines = wrap(DISP.split(" "), fontQ, maxw)
    lh = int(size * 1.5)
    if len(lines) <= 5 and all(wlen(" ".join(l), fontQ) <= maxw for l in lines) and len(lines) * lh <= 500:
        break
space_w = wlen(" ", fontQ)

AU = AUTHOR.upper()
asz = max(22, int(size * 0.34))
fontA = load(F_UP, asz, "Medium")
tr_a = asz * 0.16
auth_chars, ax = [], 0.0
for ch in AU:
    auth_chars.append((ch, ax)); ax += wlen(ch, fontA) + tr_a
auth_total = ax - tr_a if AU else 0
auth_x0 = (W - auth_total) / 2

rule_gap, auth_gap = 42, 30
block_h = len(lines) * lh
total_h = block_h + rule_gap + 6 + auth_gap + asz
y0 = (H - total_h) // 2

words = []
for li, ln in enumerate(lines):
    line_w = sum(wlen(w, fontQ) for w in ln) + space_w * (len(ln) - 1)
    x = (W - line_w) / 2
    y = y0 + li * lh
    for w in ln:
        words.append({"t": w, "x": x, "y": y}); x += wlen(w, fontQ) + space_w
rule_y = y0 + block_h + rule_gap
auth_y = rule_y + 6 + auth_gap

def ease(t): return 1 - (1 - t) ** 3
ST, WF, RISE = 0.06, 0.5, 15
q_last = (len(words) - 1) * ST
auth_start = q_last + WF * 0.5 + 0.18
reveal_end = auth_start + WF
HOLD, FOUT = 2.1, 0.6
DUR = reveal_end + HOLD + FOUT
N = int(FPS * DUR); fout_start = DUR - FOUT

def alpha_at(t, start):
    r = (t - start) / WF
    if r <= 0: return 0.0, RISE
    if r >= 1: return 1.0, 0.0
    e = ease(r); return e, (1 - e) * RISE

for fidx in range(N):
    t = fidx / FPS
    gout = 1.0 if t < fout_start else max(0.0, 1 - (t - fout_start) / FOUT)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i, wd in enumerate(words):
        a, yoff = alpha_at(t, i * ST); A = int(a * gout * 255)
        if A <= 0: continue
        od.text((wd["x"], wd["y"] - yoff), wd["t"], font=fontQ, fill=INK + (A,), anchor="la")
    if AU:
        a, yoff = alpha_at(t, auth_start); A = int(a * gout * 255)
        if A > 0:
            od.line([(W//2 - 40, rule_y - yoff), (W//2 + 40, rule_y - yoff)], fill=INK + (int(A*0.65),), width=2)
            for ch, cx in auth_chars:
                od.text((auth_x0 + cx, auth_y - yoff), ch, font=fontA, fill=INK + (A,), anchor="la")
    fr = Image.new("RGB", (W, H), BG); fr.paste(ov, (0, 0), ov)
    fr.save(os.path.join(fd, f"f{fidx:04d}.png"))

subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(fd, "f%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", OUT],
    check=True, capture_output=True)
shutil.rmtree(tmp, ignore_errors=True)
print("wrote", OUT)
```

## Adjustable knobs (only when he asks)

- Smaller or larger: change `maxw` and the `range(72, 32, -3)` ceiling.
- Faster or slower reveal: `ST` (stagger between words), `WF` (per-word fade), `HOLD` (hold time).
- Different font: swap the Lora paths, keep it an italic serif for the quote and an upright face for the author.
- Keep the output black text on white; that matches the channel's thumbnails. Do not add color, boxes, or a logo unless he asks.