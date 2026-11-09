# momentica-media
Media hosting for Instagram page @momentica.ir (posted via Metricool, brandId 7790800, timezone Asia/Tehran).
- All captions/text in Persian. Never use the "X is not just Y" construction (e.g. «نه تنها… که…», «… تنها یک … نیست؛ …است»).
- Never reproduce modern song lyrics; classical poetry (Hafez, Molana, Saadi…) is fine. Verify every verse against an online diwan (e.g. fa.wikisource.org) before publishing.
- Logo mark on every image (tools/fal/mark_gold.png on dark, full light logo on last slide).
- Daily fal carousel tool: tools/fal (see README).
- Reels: tools/reel/minimal_reel.py (v2 style, spec in its docstring). ALWAYS follow tools/reel/PLAYBOOK.md (v2) and log every reel in tools/reel/log.md. make_reel.py is the rejected v1 style — do not use it.
- Fonts: free fonts only in this public repo (Lalezar, Vazirmatn, Noto via `npm i @fontsource/lalezar @fontsource/vazirmatn @fontsource/noto-naskh-arabic` inside tools/fal). Never commit the owner's licensed fonts here.
