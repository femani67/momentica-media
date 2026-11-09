"""Build a momentica reel (1080x1920, 30fps, H.264/AAC) from a JSON spec.

Usage:  python3 make_reel.py spec.json out_dir
Produces out_dir/reel.mp4 and out_dir/cover.jpg

Two kinds:
  "note": one real-footage background + kinetic word-by-word text (the 22:00 night note)
  "game": "stop the video" game (18:30): question over moving footage, then options flash 0.4s each (x2), then CTA

Spec (note):
{"kind":"note","duration":9,
 "bg":{"url":"https://assets.mixkit.co/videos/2846/2846-1080.mp4","ss":2,"crop_x":"center"|int},
 "music":"https://assets.mixkit.co/music/22/22.mp3",
 "phrases":[{"start":0.3,"end":3.6,"lines":[[["هر",""],["شب",""]],[["دلم","a big"]]]}, ...],
 "cta":{"start":6.6,"lines":[[["بفرستش","big"]],[["برای","sm"],["کسی","sm"],["که","sm"]],[["…","a sm"]]]},
 "cover_lines":["هر شب","یه گوشه از <a>دلم</a>","<a>بیدار می‌مونه…</a>"]}
Spec (game):
{"kind":"game","question":[["حس","big"],["امروزت",""],["کدومه؟","a"]],
 "options":[{"word":"دلتنگ","url":".../2846-720.mp4","ss":3}, ... 8 items],
 "music":"...","cta":{...as above...},"cover_lines":[...]}
Word classes: "" normal, "a" accent(gold), "big", "sm", combine with space.
"""
import base64, io, json, pathlib, subprocess, sys, urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
FAL = HERE.parent / "fal"
FS = FAL / "node_modules/@fontsource"
FPS = 30
CHROME = "/usr/bin/google-chrome" if pathlib.Path("/usr/bin/google-chrome").exists() else None

def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def tint(path, hexc):
    rgb = tuple(int(hexc.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    im = Image.open(path).convert('RGBA'); out = Image.new('RGBA', im.size, rgb + (255,)); out.putalpha(im.split()[3])
    bio = io.BytesIO(); out.save(bio, 'PNG'); return base64.b64encode(bio.getvalue()).decode()

FONT = FS / "lalezar/files/lalezar-arabic-400-normal.woff2"
LATIN = FS / "vazirmatn/files/vazirmatn-latin-400-normal.woff2"
WHITE, GOLD = "#FFF6EA", "#E6BE8A"

def css(size=135):
    return f"""@font-face{{font-family:K;src:url(data:font/woff2;base64,{b64(FONT)})}}@font-face{{font-family:VL;src:url(data:font/woff2;base64,{b64(LATIN)})}}
*{{margin:0;padding:0}}html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden}}
body{{direction:rtl;color:{WHITE};font-family:K}}
.ph{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:330px 80px}}
.ln{{line-height:1.22;margin:2px 0}}
.w{{display:inline-block;font-size:{size}px;text-shadow:0 6px 28px rgba(0,0,0,.6);margin:0 9px}}
.a{{color:{GOLD}}}.big{{font-size:{int(size*1.45)}px}}.sm{{font-size:{int(size*0.66)}px}}
@keyframes pop{{0%{{opacity:0;transform:scale(.3) translateY(40px);filter:blur(8px)}}60%{{opacity:1;filter:blur(0)}}100%{{opacity:1;transform:none}}}}
@keyframes out{{to{{opacity:0;transform:scale(.94)}}}}@keyframes fin{{from{{opacity:0}}to{{opacity:1}}}}@keyframes show{{from{{opacity:1}}to{{opacity:1}}}}
.foot{{position:absolute;bottom:250px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px}}
.foot img{{height:70px}}.foot span{{font-family:VL;font-size:30px;letter-spacing:3px;color:{GOLD};direction:ltr}}
.logo{{width:600px;margin-top:70px}}
.fl{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}}.fw{{font-size:230px;text-shadow:0 8px 40px rgba(0,0,0,.6)}}"""

def phrase_html(ph, step=0.3, logo=None):
    t = ph["start"]; lines = []
    for line in ph["lines"]:
        ws = []
        for w, cls in line:
            ws.append(f'<span class="w {cls}" style="animation:pop .55s cubic-bezier(.2,1.6,.4,1) {t:.2f}s both">{w}</span>'); t += ph.get("step", step)
        lines.append('<div class="ln">' + " ".join(ws) + '</div>')
    lg = f'<img class="logo" src="data:image/png;base64,{logo}" style="animation:fin .6s ease {t+0.15:.2f}s both">' if logo else ""
    end = ph.get("end", 99)
    return f'<div class="ph" style="animation:out .4s ease-in {end:.2f}s both">{"".join(lines)}{lg}</div>'

def render_frames(html, n, out):
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.set_content(html); pg.wait_for_timeout(700)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for i in range(n):
            pg.evaluate(f"document.getAnimations().forEach(a=>{{a.currentTime={i*1000/FPS+1}}})")
            pg.screenshot(path=str(out / f"f{i:04d}.png"), omit_background=True)
        b.close()

def fetch(url, dest):
    if not dest.exists():
        urllib.request.urlretrieve(url, dest)
    return dest

def sh(cmd): subprocess.run(cmd, check=True)

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart"]
GRADE = "fps=30,eq=brightness=-0.06:saturation=0.92,vignette=PI/4,drawbox=c=black@0.30:t=fill"

def vf_crop(crop_x):
    if crop_x in (None, "center"):
        return "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    return f"scale=-2:1920,crop=1080:1920:{int(crop_x)}:0"

def cover(spec, out, bgframe):
    lines = "<br>".join(l.replace("<a>", f'<span style="color:{GOLD}">').replace("</a>", "</span>") for l in spec["cover_lines"])
    mark = tint(FAL / "mark_gold.png", GOLD)
    html = f'''<html><head><meta charset="utf-8"><style>{css()}</style></head><body>
<div style="position:absolute;inset:0;background:url(data:image/jpeg;base64,{b64(bgframe)}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,18,29,.55),rgba(21,28,44,.72) 50%,rgba(13,18,29,.55))"></div>
<div style="position:absolute;left:44px;right:44px;top:284px;bottom:284px;border:1.5px solid rgba(196,154,108,.5);border-radius:6px"></div>
<div class="ph"><div style="font-size:{spec.get('cover_size',120)}px;line-height:1.3;text-shadow:0 6px 28px rgba(0,0,0,.55)">{lines}</div></div>
<div class="foot" style="bottom:340px"><img src="data:image/png;base64,{mark}"><span>MOMENTICA.IR</span></div></body></html>'''
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.set_content(html); pg.wait_for_timeout(700)
        pg.screenshot(path=str(out / "cover.png")); b.close()
    Image.open(out / "cover.png").convert("RGB").save(out / "cover.jpg", quality=92); (out / "cover.png").unlink()

def build(spec, out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    dur = spec.get("duration", 9); n = int(dur * FPS)
    mark = tint(FAL / "mark_gold.png", GOLD); logo = tint(FAL / "logo_light.png", WHITE)
    music = fetch(spec["music"], tmp / "music.mp3")
    cta = dict(spec["cta"]); cta.setdefault("step", 0.18)
    foot_end = cta["start"] - 0.3
    foot = f'<div class="foot" style="animation:fin .5s ease .1s both, out .3s ease-in {foot_end:.2f}s both"><img src="data:image/png;base64,{mark}"><span>MOMENTICA.IR</span></div>'
    if spec["kind"] == "note":
        body = "".join(phrase_html(p) for p in spec["phrases"]) + phrase_html(cta, logo=logo) + foot
        bg = fetch(spec["bg"]["url"], tmp / "bg.mp4")
        bgv = f"[0:v]{vf_crop(spec['bg'].get('crop_x'))},{GRADE},drawbox=c=black@0.3:t=fill:enable='gte(t,{cta['start']-0.2})',format=yuv420p[bg]"
        inputs = ["-stream_loop", "2", "-ss", str(spec["bg"].get("ss", 0)), "-i", str(bg)]
        sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(spec["bg"].get("ss", 0) + 1), "-i", str(bg), "-frames:v", "1",
            "-vf", vf_crop(spec['bg'].get('crop_x')) + ",eq=brightness=-0.08:saturation=0.85", str(tmp / "frame.jpg")])
    else:  # game
        opts = spec["options"]; seg = 12  # frames per option
        q_end = spec.get("q_frames", 45)  # question shown over first clip for 1.5s
        segs = []
        for i, o in enumerate(opts):
            src = fetch(o["url"], tmp / f"o{i}.mp4")
            dst = tmp / f"s{i}.mp4"
            sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(o.get("ss", 1)), "-i", str(src), "-vf",
                vf_crop(o.get("crop_x")) + "," + GRADE + ",setsar=1,format=yuv420p", "-frames:v", str(seg), "-an", "-c:v", "libx264", "-crf", "18", str(dst)])
            segs.append(dst)
        first = fetch(opts[0]["url"], tmp / "o0.mp4")
        sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "0", "-i", str(first), "-vf",
            vf_crop(opts[0].get("crop_x")) + "," + GRADE + ",setsar=1,format=yuv420p", "-frames:v", str(q_end), "-an", "-c:v", "libx264", "-crf", "18", str(tmp / "q.mp4")])
        order = [tmp / "q.mp4"] + segs + segs
        used = q_end + 2 * seg * len(opts)
        tail_frames = max(n - used, 60); n = used + tail_frames; dur = n / FPS
        last = fetch(opts[-1]["url"], tmp / f"o{len(opts)-1}.mp4")
        sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "0", "-i", str(last), "-vf",
            vf_crop(opts[-1].get("crop_x")) + "," + GRADE + ",drawbox=c=black@0.35:t=fill,setsar=1,format=yuv420p", "-frames:v", str(tail_frames), "-an", "-c:v", "libx264", "-crf", "18", str(tmp / "t.mp4")])
        order.append(tmp / "t.mp4")
        lst = tmp / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in order))
        sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp / "bg.mp4")])
        qph = {"start": 0.05, "step": 0.1, "end": q_end / FPS - 0.3, "lines": [spec["question"], [["نگهش", "sm"], ["دار", "sm"], ["و", "sm"], ["انتخاب", "sm"], ["کن", "sm"]]]}
        flashes = ""; f0 = q_end
        for r in range(2):
            for o in opts:
                flashes += f'<div class="fl" style="animation:show .4s linear {f0/FPS:.4f}s"><div class="fw">{o["word"]}</div></div>'; f0 += seg
        cta["start"] = f0 / FPS + 0.15
        foot = foot.replace(f"{foot_end:.2f}s both\"", f"{dur+5:.2f}s both\"")
        body = phrase_html(qph) + flashes + phrase_html(cta, logo=logo) + foot
        bgv = f"[0:v]noise=alls=4:allf=t,format=yuv420p[bg]"
        inputs = ["-i", str(tmp / "bg.mp4")]
        sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "0.5", "-i", str(tmp / "q.mp4"), "-frames:v", "1", str(tmp / "frame.jpg")])
    html = f'<html><head><meta charset="utf-8"><style>{css(spec.get("size",135))}</style></head><body>{body}</body></html>'
    frames = tmp / "frames"; render_frames(html, n, frames)
    fade_out = max(dur - 1.3, 0.5)
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-framerate", str(FPS), "-i", str(frames / "f%04d.png"), "-i", str(music),
        "-filter_complex", f"{bgv};[1:v]format=rgba[k];[bg][k]overlay,format=yuv420p[v];[2:a]atrim=0:{dur},afade=t=in:d=0.6,afade=t=out:st={fade_out}:d=1.2,volume=0.85[au]",
        "-map", "[v]", "-map", "[au]", "-t", f"{dur:.3f}", *ENC, str(out / "reel.mp4")])
    cover(spec, out, tmp / "frame.jpg")
    subprocess.run(["rm", "-rf", str(tmp)])
    return out / "reel.mp4"

if __name__ == "__main__":
    print(build(json.loads(pathlib.Path(sys.argv[1]).read_text()), sys.argv[2]))
