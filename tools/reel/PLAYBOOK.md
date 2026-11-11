# momentica reel playbook — v2 (2026-11-09), updated 2026-11-11

## Owner feedback 2026-11-11 (overrides the "small calm text" look below)
The minimal small-text-on-stock-footage reels all look alike and don't get shared. Goal = SHARES + comments, like high-share pages.
- Text must be BIG and readable in 2s (bold Vazirmatn 900 headline), not tiny lines in the sky.
- Build the share into the video itself: on-screen «اینو بفرست برای کسی که…» / a relatable chat-bubble moment («ارسال نشد»), a tag prompt in the caption («اسمش رو تگ کن»).
- Share-driven formats: S1 send-to-someone (big text), S2 chat bubbles / unsent message, plus F2 dialogue (best of the old ones). Every day must look visibly different (layout, colour, font size), not only a different clip.
- If the owner sends screenshots of viral reels, or adds viral pages as Metricool competitors (IGCR metrics), copy their structure first.

The owner rejected the v1 look (dark overlay, big bold popping text, framed cover, big end card) as repetitive.
**All new reels use tools/reel/minimal_reel.py** (v1 make_reel.py is kept only for reference).

## What the owner's reference reels have in common (5 viral examples, 3K–99K likes)
1. Real, natural-colour footage that feels like a real moment (moon behind rain clouds, sun rays through clouds, sunset in a car side-mirror, a full orange moon). No dark overlay, no heavy grading.
2. Little or no text. When there is text it is small, calm, placed in the empty sky area, with at most ONE big word (e.g. «دفاع»). Or a dense typographic block on a plain dark background (one format).
3. Tiny page signature at the bottom. No frame, no end card, no big logo.
4. Themes: hope / God / fate (قسمت), longing, love, night, rain, the moon, the road.
5. The caption carries the story/CTA; the video stays quiet.

## Research notes (hooks)
- 3-second hold is the main ranking signal: reels keeping 70–85% past 3s get ~2.2x views; under 60% gets throttled. Our data: night note 62% (good), game reel 38% (static intro = bad).
- Instagram's head says polished aesthetics now read as cheap; authentic, real-moment footage wins.
- Loops under ~7–9s get replayed more; most views come from non-followers, so shares/DM sends matter most.

## Hooks to use (rotate, never the same two days running)
- **Image hook**: the first frame is already striking (moon, rays, rain on glass, mirror sunset) — text optional.
- **Dialogue hook**: «گفت: … / گفتم: …» (mahsophoto style).
- **Timestamp hook**: «۲۲:۲۲ و هنوز بیدارم…» / «۱۸:۱۸ چه بارونی…» small, top.
- **Direct-address hook**: «اگه این رو می‌بینی…» / «یکی هست که…».
- **One-big-word hook**: small line + one huge word + small line (kimia_gaar «دفاع» style).

## Formats (rotate; each day's two reels must use two DIFFERENT formats, and differ from the previous day's)
F1 Quote-on-sky: bright sky/sea/clouds footage, white small text + one big word, text in sky area.
F2 Night dialogue: moon/night sky, small «گفت/گفتم» block above the subject, accent colour on one word.
F3 Silent moment: real POV footage (rain on window, road at sunset, mirror sunset, sea) with NO on-screen text except maybe a tiny timestamp; the line goes in the caption. 7s, loops.
F4 Typography block: bg "color:#2b313b" (or another muted dark tone), 4–6 lines of dense large text (class "block"), original words, light grey text.
F5 Timestamp/POV: small timestamp line + 1–2 short lines over rain/night city/window footage.

## Rules
- 7–10s. First visual/line by 0.3s. Never open on a plain static card (except F4, where the text itself is the image and must appear immediately).
- REAL footage only (no CGI/animated clips). Mixkit `videoFree` clips only (check JSON-LD license). Natural colours: grade at most `eq=saturation=1.0-1.08:brightness=-0.03..0.03`.
- Make sure the subject (moon, sun, mirror) doesn't sit under the text: crop or pre-scale (`pre_vf`, `crop_vf`) to move it.
- Text: ORIGINAL Persian (or verified classical poetry / folk proverb). Never song lyrics. Never the "X is not just Y" construction. Simple spoken Persian.
- Never reuse a clip used in the last 7 days (see log.md). Look for new real clips on mixkit topic pages (sky, clouds, moon, rain, sea, road, driving, sunset, city night, window, candle, forest, snow, coffee).
- Music: Mixkit instrumental (`musicFree`) — piano/soft. Rotate tracks.
- Fonts in automation: free Vazirmatn 300 (small) + 900 (big word) — defaults of minimal_reel.py. (Owner's licensed fonts Kahroba/Lahzeh are NOT in this repo.)
- Caption: line 1 = the hook/line; then «بفرستش برای کسی که …»; one emoji comment prompt; 5–7 hashtags incl. #momentica.
- Look at frames at 0.5s, middle, end before scheduling: readable, subject not covered, signature visible.

## Review loop
Every run: read last 3 days' reel metrics (views, reach, shares, saves, >3s rate, avg watch). Log them in log.md and favour the format/hook with the most shares + highest 3s rate, while still rotating.

## Verified real Mixkit clips (free)
sky/clouds: 26108, 51102, 51105 · moon: 48025 (pre_vf scale=-2:2600 + crop to move moon down), 4433, 47299 · rain on window: 2846 · sea: 1164 (vertical), 4119 sunset sea · road/driving: 4852, 45312 autumn road, 27717 night drive · couple sunset 4664 · flowers 1168 · coffee 236 · autumn leaves 10050
URL: https://assets.mixkit.co/videos/<id>/<id>-1080.mp4 (or -720). Music: 22, 168, 493 → https://assets.mixkit.co/music/<id>/<id>.mp3
