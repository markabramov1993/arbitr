#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, subprocess, wave
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
VOICE_SRC=ROOT/"voiceover_text"; VOICE=ROOT/"voiceover"; VIS=ROOT/"visuals"
VOICE.mkdir(exist_ok=True); VIS.mkdir(exist_ok=True)

def font(size,bold=False):
    paths=[
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
      "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

COLORS={"cyan":"#4ee8ff","green":"#61e294","amber":"#ffca58","red":"#ff6685","purple":"#b28dff"}
BG="#07111d"; PANEL="#0f2032"; TEXT="#f4f8ff"; MUTED="#9db0c7"

def card(path,w,h,title,subtitle,accent):
    im=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(im)
    c=COLORS.get(accent,COLORS["cyan"])
    d.rounded_rectangle((80,80,w-80,h-80),radius=42,fill=PANEL,outline=c,width=5)
    d.text((130,135),"RUSTCHAIN · BOUNTY PIPELINE",font=font(34,True),fill=c)
    d.text((130,h//2-90),title,font=font(68,True),fill=TEXT)
    d.text((130,h//2+15),subtitle,font=font(38),fill=MUTED)
    d.line((130,h-190,w-130,h-190),fill="#29445e",width=3)
    d.text((130,h-150),"source-backed · no price claim · no stock media",font=font(28),fill=MUTED)
    im.save(path)

specs=json.loads((ROOT/"visual_specs.json").read_text())
for s in specs: card(VIS/s["file"],1920,1080,s["title"],s["subtitle"],s["accent"])

thumbs=[
 ("thumbnail.png","PAID ≠ SETTLED","BOUNTY → VERIFIED → PENDING → WALLET","cyan"),
 ("thumbnail-alt-1.png","WHERE IS THE RTC?","FOLLOW THE PAYOUT EVIDENCE","green"),
 ("thumbnail-alt-2.png","COUNT THE RECEIPT","NOT THE STICKER PRICE","amber"),
]
for fn,t,st,a in thumbs: card(ROOT/fn,1280,720,t,st,a)

durations=[]
for src in sorted(VOICE_SRC.glob("*.txt")):
    out=VOICE/(src.stem+".wav")
    subprocess.run(["espeak-ng","-v","en-us","-s","145","-w",str(out),src.read_text()],check=True)
    with wave.open(str(out),"rb") as w:
        dur=w.getnframes()/w.getframerate()
    durations.append((src.stem,dur,out))

start=0.0
lines=["# Assembly Map","","Generated from actual narration WAV durations.",""]
for idx,(name,dur,out) in enumerate(durations,1):
    end=start+dur
    vis=specs[min(idx-1,len(specs)-1)]["file"]
    lines += [f"## {start:05.1f}–{end:05.1f} — Section {idx}",
              f"- Voice: `voiceover/{out.name}`",
              f"- Primary visual: `visuals/{vis}`",
              "- Edit: slow 3–5% push-in; hard cut at section boundary; burn subtitles from narration source.",""]
    start=end
(ROOT/"assembly.md").write_text("\n".join(lines)+"\n")

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert 180 <= start <= 480, f"narration duration {start:.2f}s out of range"
assert len(list(VIS.glob("*.png"))) == 8
for p in VIS.glob("*.png"):
    assert Image.open(p).size==(1920,1080)
for p in [ROOT/"thumbnail.png",ROOT/"thumbnail-alt-1.png",ROOT/"thumbnail-alt-2.png"]:
    assert Image.open(p).size==(1280,720)
print("TYPE_A_PACKAGE_VALIDATION=PASS")
print(f"VOICEOVER_SECTIONS={len(durations)}")
print(f"VOICEOVER_DURATION_SECONDS={start:.2f}")
print("VISUALS=8 @ 1920x1080")
print("THUMBNAILS=3 @ 1280x720")
for _,dur,p in durations: print(f"WAV={p.name} duration={dur:.2f} sha256={sha(p)}")
