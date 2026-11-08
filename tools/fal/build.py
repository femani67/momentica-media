import json, sys, base64, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
def b64(p): return base64.b64encode((HERE / p).read_bytes()).decode()

FONTS = HERE / "node_modules/@fontsource"
css_fonts = f"""
@font-face{{font-family:Vazir;font-weight:300;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-300-normal.woff2')})}}
@font-face{{font-family:Vazir;font-weight:400;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-400-normal.woff2')})}}
@font-face{{font-family:Vazir;font-weight:700;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-700-normal.woff2')})}}
@font-face{{font-family:Naskh;font-weight:400;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/noto-naskh-arabic/files/noto-naskh-arabic-arabic-400-normal.woff2')})}}
@font-face{{font-family:Naskh;font-weight:600;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/noto-naskh-arabic/files/noto-naskh-arabic-arabic-600-normal.woff2')})}}
@font-face{{font-family:VazirL;font-weight:400;src:url(data:font/woff2;base64,{b64('node_modules/@fontsource/vazirmatn/files/vazirmatn-latin-400-normal.woff2')})}}
"""
MARK = b64("mark_gold.png")
LOGO = b64("logo_light.png")

BASE = css_fonts + """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;direction:rtl;font-family:Vazir,VazirL;color:#F4EADA;
 background:radial-gradient(120% 80% at 50% 0%,#24304a 0%,#151c2c 55%,#0d121d 100%);position:relative}
.frame{position:absolute;inset:44px;border:1.5px solid rgba(196,154,108,.45);border-radius:6px}
.frame:after{content:"";position:absolute;inset:10px;border:1px solid rgba(196,154,108,.18);border-radius:4px}
.content{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:150px 120px;text-align:center}
.foot{position:absolute;bottom:78px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px;opacity:.9}
.foot img{height:54px}.foot span{font-family:VazirL;font-size:24px;letter-spacing:2px;direction:ltr;color:#C49A6C;font-weight:400}
.top{position:absolute;top:92px;left:0;right:0;text-align:center;font-size:26px;color:#C49A6C;letter-spacing:1px}
.gold{color:#C49A6C}
.orn{width:220px;height:2px;background:linear-gradient(90deg,transparent,#C49A6C,transparent);margin:34px auto}
.beyt{font-family:Naskh;font-size:54px;line-height:1.75;font-weight:400}
.beyt .m{display:block}
.beyt + .beyt{margin-top:56px}
.dots{position:absolute;bottom:150px;left:0;right:0;display:flex;justify-content:center;gap:12px}
.dots i{width:10px;height:10px;border-radius:50%;background:rgba(196,154,108,.3)}.dots i.on{background:#C49A6C}
"""

def page(inner, idx, total, foot=True, top=None):
    dots = "".join(f'<i class="{"on" if i==idx else ""}"></i>' for i in range(total))
    f = f'<div class="foot"><img src="data:image/png;base64,{MARK}"><span>MOMENTICA.IR</span></div>' if foot else ""
    t = f'<div class="top">{top}</div>' if top else ""
    return f'<html><head><meta charset="utf-8"><style>{BASE}</style></head><body><div class="frame"></div>{t}<div class="content">{inner}</div><div class="dots">{dots}</div>{f}</body></html>'

def beyts(pairs):
    return "".join(f'<div class="beyt"><span class="m">{a}</span><span class="m gold">{b}</span></div>' for a,b in pairs)

def render(data, outdir):
    outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    slides = []
    slides.append(("cover", f'''
      <div style="font-size:30px;color:#C49A6C;letter-spacing:2px">فال حافظ امروز</div>
      <div class="orn"></div>
      <div style="font-family:Naskh;font-size:112px;font-weight:600;line-height:1.3">نیت کن…</div>
      <div style="font-size:36px;font-weight:300;margin-top:40px;line-height:1.9;opacity:.92">یه لحظه چشماتو ببند<br>به آرزوت فکر کن</div>
      <div style="font-size:34px;margin-top:70px;color:#C49A6C;font-weight:400">و ورق بزن ←</div>'''))
    for grp in data["verse_slides"]:
        slides.append(("verse", beyts(grp)))
    slides.append(("tabir", f'''
      <div style="font-size:30px;color:#C49A6C;letter-spacing:2px">تعبیر فال تو</div>
      <div class="orn"></div>
      <div style="font-size:42px;line-height:2;font-weight:300">{data["tabir"]}</div>'''))
    slides.append(("cta", f'''
      <div style="font-size:44px;line-height:1.9;font-weight:400">{data["cta"]}</div>
      <div class="orn"></div>
      <div style="font-size:30px;line-height:1.9;font-weight:300;opacity:.85">هر روز یه فال تازه<br>پیج رو دنبال کن تا فالِ فردات رو از دست ندی</div>
      <img src="data:image/png;base64,{LOGO}" style="width:620px;margin-top:80px">'''))
    total = len(slides)
    top = f'غزل {data["ghazal_no"]} · حافظ'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width":1080,"height":1350})
        files = []
        for i,(kind,inner) in enumerate(slides):
            html = page(inner, i, total, foot=(kind!="cta"), top=(top if kind in("verse","tabir") else None))
            pg.set_content(html); pg.wait_for_timeout(300)
            fn = outdir / f"slide{i+1}.png"; pg.screenshot(path=str(fn)); files.append(str(fn))
        b.close()
    return files

if __name__ == "__main__":
    data = json.loads(pathlib.Path(sys.argv[1]).read_text())
    print(render(data, sys.argv[2]))
