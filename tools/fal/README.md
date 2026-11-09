# Daily Hafez fal carousel

Setup (fresh machine):
    cd tools/fal && npm i @fontsource/vazirmatn @fontsource/noto-naskh-arabic @fontsource/lalezar && pip install playwright --break-system-packages
Build:
    python3 build.py ghazal.json out_dir   # writes slide1..N.png (1080x1350)

ghazal.json format: see example-g255.json (verse_slides = 3 slides x 2 beyts, tabir, cta, ghazal_no in Persian digits).
used_ghazals.txt: ghazal numbers already posted — never repeat.
Posts go in posts/YYYY-MM-DD-fal-NNN/ as slide1..6.jpg (JPEG q92) + caption.txt.
Media URLs for Metricool: https://raw.githubusercontent.com/Femani67/momentica-media/<commit-sha>/posts/...
