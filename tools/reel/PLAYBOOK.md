# momentica reel playbook (based on real results)

## Why the 2026-11-08 22:00 night-note reel won (820 views, 685 reach, 5 shares, 3 saves on a ~40-follower page)
| signal | night note 22:00 | feel game 18:30 | fal carousel 10:00 |
|---|---|---|---|
| views / reach | 820 / 685 | 278 / 240 | 129 / 45 |
| >3s view rate | 61.6% | 38.3% | – |
| avg watch | 5.6s of 12s | 6.4s of 12s | – |
| shares | 5 | 2 | 2 |

What worked:
1. **Instant hook on moving real footage** – first word at 0.3s over rain video. The game reel opened on a static navy card for 2s and lost 60% in 3s.
2. **One relatable longing feeling (دلتنگی/عاشقانه) in simple spoken Persian** – something people want to send to *one specific person*.
3. **Explicit DM-share trigger tied to the text**: «بفرستش برای کسی که …» → shares are what pushed it to non-followers.
4. **Night slot (22:00)** – emotional content when people scroll in bed.
5. Kinetic word-by-word pop text (Lalezar, white + gold key word), real footage, soft piano, logo end card.
Weakness: viewers left around 5–6s → keep reels 8–9s so they loop.

## Rules for every reel
- 1080x1920, 8–11s. First text on screen by 0.3s. Never open on a static/plain card.
- Background = REAL footage only (rain, sea, road, sky, city night, candle, coffee, nature). Never CGI/animated clips. Mixkit clips with license `videoFree` only (check JSON-LD `license` on the mixkit page).
- Music: Mixkit instrumental (`musicFree`), piano/soft for notes, light/upbeat for games. Never copyrighted songs.
- Text: max ~10 words before the CTA, colloquial Persian, one gold accent word (the emotional core). Never use the "X is not just Y" construction (e.g. «نه تنها… که…»).
- End card (last ~2.5s): «بفرستش برای کسی که …» (night note) / «تو کامنت بنویس + بفرستش برای رفیقت» (game) + full logo.
- Cover: same navy/gold frame style (make_reel.py does it). Grid must stay cohesive.
- Caption: line 1 = the hook text; then share CTA; then a one-emoji/one-word comment prompt; 5–7 hashtags incl. #momentica.

## 22:00 night note (کلمه‌به‌کلمه دلنوشته)
Two short phrases + CTA. Phrase 1 = the feeling (dlتنگی/عشق/انتظار/خاطره), phrase 2 = the emotional punch. Rotate background clip every night (never same clip two nights in a row). Write ORIGINAL lines (never song lyrics).

## 18:30 "stop the video" game (نگهش دار و انتخاب کن)
Question over the first moving clip (≈2s), 8 options × 0.4s, shown twice, then CTA. Rotate the question in this order (continue from tools/reel/log.md):
1. حس امروزت کدومه؟  2. امروز دلت چی می‌خواد؟  3. کلمه‌ی امروزت چیه؟  4. الان دلت کجاست؟  5. پیام امروز برای تو (short sentences as options)  6. بیت تو کدومه؟ (short classical half-beyts, verified)  7. امشب حالت چطوره؟
Change the 8 options and clips each time; each option word must match its clip.

## Verified real Mixkit clips (free license)
2846 rain on window · 1164 sea waves (vertical) · 4852 empty road · 4664 couple at sunset · 4119 sunset over sea · 4433 full moon · 1168 flowers (vertical) · 236 coffee · 10050 autumn leaves falling (real) · 45271 autumn forest pan
URL pattern: https://assets.mixkit.co/videos/<id>/<id>-720.mp4 (or -1080). Find more on https://mixkit.co/free-stock-video/<topic>/ (parse JSON-LD VideoObject, keep license containing `videoFree`).
Music: piano 22, night sky 168, upbeat 493 → https://assets.mixkit.co/music/<id>/<id>.mp3 (more on https://mixkit.co/free-stock-music/…).

## Review loop
Each run: read the last 3 days of reel metrics in Metricool (views, reach, shares, saves, >3s view rate, avg watch). Append a line to tools/reel/log.md and lean toward whatever got the most shares.
