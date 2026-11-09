import base64,sys,json,pathlib,subprocess
sys.path.insert(0,'/home/claude/momentica-media/tools/reel')
import make_reel as M
U='/home/claude/userfonts/'
def b(p): return base64.b64encode(open(p,'rb').read()).decode()
def build(spec,out):
    out=pathlib.Path(out);out.mkdir(exist_ok=True)
    mark=M.tint(M.FAL/'mark_gold.png',spec['mark'])
    lines=''
    t=spec.get('t0',0.4)
    for txt,cls in spec['lines']:
        lines+=f'<div class="l {cls}" style="animation:fade 1.1s ease {t:.2f}s both">{txt}</div>'; t+=spec.get('gap',0.55)
    html=f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:S;src:url(data:font/ttf;base64,{b(U+spec.get('small_font','13ff866b-Lahzeh-Regular.ttf'))})}}
@font-face{{font-family:B;src:url(data:font/ttf;base64,{b(U+spec.get('big_font','b5e73218-KAHROBA-FD-BL.TTF'))})}}
@font-face{{font-family:VL;src:url(data:font/woff2;base64,{M.b64(M.LATIN)})}}
*{{margin:0;padding:0}}html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden}}
body{{direction:rtl;color:{spec['color']};font-family:S}}
.box{{position:absolute;left:0;right:0;top:{spec['top']}px;text-align:center}}
.l{{font-size:{spec.get('small',50)}px;line-height:1.6;text-shadow:{spec.get('shadow','none')}}}
.big{{font-family:B;font-size:{spec.get('big',150)}px;line-height:1.15;margin:10px 0}}
.acc{{color:{spec.get('accent',spec['color'])}}}
@keyframes fade{{0%{{opacity:0;filter:blur(10px);transform:translateY(14px)}}100%{{opacity:1;filter:blur(0);transform:none}}}}
.sig{{position:absolute;bottom:{spec.get('sig_bottom',330)}px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px;opacity:.85;animation:fade 1s ease .2s both}}
.sig img{{height:46px}}.sig span{{font-family:VL;font-size:22px;letter-spacing:4px;color:{spec['mark']};direction:ltr}}
</style></head><body><div class="box">{lines}</div><div class="sig"><img src="data:image/png;base64,{mark}"><span>MOMENTICA.IR</span></div></body></html>'''
    n=int(spec['duration']*30); fr=out/'frames'
    M.render_frames(html,n,fr)
    bg=spec['bg']; music=spec['music']
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-stream_loop','2','-ss',str(spec.get('ss',0)),'-i',bg,'-framerate','30','-i',str(fr/'f%04d.png'),'-i',music,
     '-filter_complex',f"[0:v]{M.vf_crop(spec.get('crop_x'))},fps=30,{spec.get('grade','eq=saturation=1.02')},format=yuv420p[bg];[1:v]format=rgba[k];[bg][k]overlay,format=yuv420p[v];[2:a]atrim=0:{spec['duration']},afade=t=in:d=0.8,afade=t=out:st={spec['duration']-1.2}:d=1.2,volume=0.8[au]",
     '-map','[v]','-map','[au]','-t',str(spec['duration']),*M.ENC,str(out/'reel.mp4')],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-sseof','-0.5','-i',str(out/'reel.mp4'),'-frames:v','1','-q:v','2',str(out/'cover.jpg')],check=True)
    subprocess.run(['rm','-rf',str(fr)])
if __name__=='__main__': build(json.load(open(sys.argv[1])),sys.argv[2])
