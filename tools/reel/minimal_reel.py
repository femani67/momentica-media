"""Minimal real-footage reel (the style the owner chose on 2026-11-09).
Usage: python3 minimal_reel.py spec.json outdir  -> outdir/reel.mp4, outdir/cover.jpg

spec keys:
  duration (s, 7-10), bg: path/URL to video OR "color:#2b313b" (solid, for typography blocks),
  ss (start sec), crop_x ("center" | int px after scaling to 1920 high), pre_vf (optional ffmpeg filter applied before crop, e.g. "scale=-2:2600" + crop_y),
  music: path/URL (Mixkit musicFree), color (text), accent, mark (signature color), top (px from top for text box),
  small (px), big (px), t0 (first line time), gap (sec between lines), shadow (css text-shadow),
  grade (ffmpeg eq filter; keep colors natural), sig_bottom (px),
  lines: [[text, cls], ...]  cls: "" small | "big" big word | "acc" accent color | "block" dense typography block line
  fonts: {"small": path, "big": path}  (defaults: free Vazirmatn 300 / 900 from @fontsource in tools/fal/node_modules)
No end card, no frame, no big logo: only a small MOMENTICA.IR signature.
"""
import base64, sys, json, pathlib, subprocess, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_reel as M

VZ = M.FS / "vazirmatn/files"
DEF_SMALL = VZ / "vazirmatn-arabic-300-normal.woff2"
DEF_BIG = VZ / "vazirmatn-arabic-900-normal.woff2"

def b(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def fmt(p): return "truetype" if str(p).lower().endswith(("ttf", "otf")) else "woff2"

def get(src, tmp, name):
    if str(src).startswith("http"):
        dst = tmp / name
        if not dst.exists(): urllib.request.urlretrieve(src, dst)
        return str(dst)
    return str(src)

def build(spec, out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    fonts = spec.get("fonts", {}); fs, fb = fonts.get("small", DEF_SMALL), fonts.get("big", DEF_BIG)
    mark = M.tint(M.FAL / "mark_gold.png", spec["mark"])
    lines = ""; t = spec.get("t0", 0.3)
    for txt, cls in spec["lines"]:
        lines += f'<div class="l {cls}" style="animation:fade 1s ease {t:.2f}s both">{txt}</div>'; t += spec.get("gap", 0.5)
    html = f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:S;src:url(data:font/{fmt(fs)};base64,{b(fs)})}}
@font-face{{font-family:B;src:url(data:font/{fmt(fb)};base64,{b(fb)})}}
@font-face{{font-family:VL;src:url(data:font/woff2;base64,{M.b64(M.LATIN)})}}
*{{margin:0;padding:0}}html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden}}
body{{direction:rtl;color:{spec['color']};font-family:S}}
.box{{position:absolute;left:70px;right:70px;top:{spec['top']}px;text-align:center}}
.l{{font-size:{spec.get('small',50)}px;line-height:1.6;text-shadow:{spec.get('shadow','none')}}}
.big{{font-family:B;font-size:{spec.get('big',150)}px;line-height:1.15;margin:10px 0}}
.block{{font-family:B;font-size:{spec.get('big',150)}px;line-height:.98;letter-spacing:-2px}}
.acc{{color:{spec.get('accent',spec['color'])}}}
@keyframes fade{{0%{{opacity:0;filter:blur(10px);transform:translateY(14px)}}100%{{opacity:1;filter:blur(0);transform:none}}}}
.sig{{position:absolute;bottom:{spec.get('sig_bottom',300)}px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px;opacity:.85;animation:fade 1s ease .2s both}}
.sig img{{height:46px}}.sig span{{font-family:VL;font-size:22px;letter-spacing:4px;color:{spec['mark']};direction:ltr}}
</style></head><body><div class="box">{lines}</div><div class="sig"><img src="data:image/png;base64,{mark}"><span>MOMENTICA.IR</span></div></body></html>'''
    dur = spec["duration"]; n = int(dur * 30); fr = tmp / "frames"
    M.render_frames(html, n, fr)
    music = get(spec["music"], tmp, "music.mp3")
    if str(spec["bg"]).startswith("color:"):
        col = spec["bg"][6:].replace("#", "0x")
        bgin = ["-f", "lavfi", "-i", f"color=c={col}:s=1080x1920:r=30:d={dur}"]
        bgv = "[0:v]noise=alls=5:allf=t,format=yuv420p[bg]"
    else:
        bg = get(spec["bg"], tmp, "bg.mp4")
        bgin = ["-stream_loop", "3", "-ss", str(spec.get("ss", 0)), "-i", bg]
        pre = (spec["pre_vf"] + ",") if spec.get("pre_vf") else ""
        crop = spec.get("crop_vf") or M.vf_crop(spec.get("crop_x"))
        bgv = f"[0:v]{pre}{crop},fps=30,{spec.get('grade','eq=saturation=1.02')},format=yuv420p[bg]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *bgin, "-framerate", "30", "-i", str(fr / "f%04d.png"), "-i", music,
        "-filter_complex", f"{bgv};[1:v]format=rgba[k];[bg][k]overlay,format=yuv420p[v];[2:a]atrim=0:{dur},afade=t=in:d=0.8,afade=t=out:st={dur-1.2}:d=1.2,volume=0.8[au]",
        "-map", "[v]", "-map", "[au]", "-t", str(dur), *M.ENC, str(out / "reel.mp4")], check=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-sseof", "-0.4", "-i", str(out / "reel.mp4"), "-frames:v", "1", "-q:v", "2", str(out / "cover.jpg")], check=True)
    subprocess.run(["rm", "-rf", str(tmp)])
    return out / "reel.mp4"

if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1])), sys.argv[2]))
