# Review report: goal-misgeneralization-in-deep-reinforcement-learning

Standing authorization covers site publication after all required checks pass; no personal review or confirmation is required. Inspect `out/video.mp4` and the page
(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against
the evidence register. Then run `paper-video approve goal-misgeneralization-in-deep-reinforcement-learning`.

## Source notes
- Quotes found in the PDF: yes. Page corrections: 0.

## Storyboard
- Provenance checks: pass.
- Science review: **accurate**.
  - [minor] s04b03.on_screen_text; d3.note: The current permeable-wall result displays 100% without the sample size n = 114 supplied by c21. The narration limits the result to the permeable-wall experiment, but displaying its sample size would make the finite experimental scope clearer.

## Web page
- Provenance checks: pass.
- Science review: **accurate**.

## Scenes
- s01: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s01-sheet.png`)
  - [minor] s01b02: The end-of-beat frame shows only heading and tag because the split comparison fades during the final 0.6 s of narration so that s01b03 opens on its own title card; the panel titles in this beat remain at size 22.
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s02-sheet.png`)
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s03-sheet.png`)
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s04-sheet.png`)
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s05-sheet.png`)
- s06: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s06-sheet.png`)

## Video
- Duration 257 s, 1920x1080.

## Short-form companion
- Checks pass: 114.20s, 1080x1920, current independent review.
  - [minor] s02b02: The narration says the agent "ran straight past the coin to the empty right wall" as a universal outcome. The paper's statement (c13) is hedged: "the agent generally ignores the coin completely and proceeds to the end of the level." The same unhedged wording appears in the description ("ran past a relocated coin").
  - [minor] s02b01: "trained to jump over saws and enemies" names obstacles that are not in the notes (c10, c12 only describe the coin at the right end next to a wall). The diagram shows only spikes, so the detail is unsupported by both the notes and the visual.
  - [minor] s05b01: The narration states the authors' prerequisite hypothesis (c08) as an unattributed fact ("Because proxy goals rely on accidental correlations during training") and says decorrelation "should help the model learn the true objective", which goes beyond the observed result (c14 only reports improved goal generalization in CoinRun). The HYPOTHESIS badge is the only attribution and is about 6 px tall at phone width.
  - [minor] s03b01: c09 is a general hypothesis that learned proxies use simpler or bias-favored features; the notes do not show the authors applying it specifically to "moving right" in CoinRun. The diagram adds "Object tracking" versus "Simple direction cue" as the feature contrast, which is not in the notes.
  - [minor] s06b02: "their theoretical framework" has no antecedent in this edit: the agents-and-devices formalism (c07, c23) is omitted, so viewers are told the limits of a framework they never saw.
  - [minor] s01b03: "master complex capabilities while learning completely unintended goals" overstates the arcade-game setting (c01, c04 speak of retained capabilities and a wrong goal or proxy), and "investigated this problem" ties the invented facility scenario of s01b01 directly to the study.
  - [minor] s06b03: The on-screen slogan "Performance is not alignment" is broader than the narrated claim (c04 says optimizing R does not guarantee the model pursues R rather than a proxy) and is not attributed.
  - [minor] s05b03: The beat is badged AUTHORS' INTERPRETATION, but it mixes an editorial mechanism ("weakens the link between rightward progress and reward") with the observed result c14 ("goal generalization improved; further randomization helped more"), so the observed part carries an interpretation label.
  - [minor] s02b02: At the cut from s02b01 (frames 1001-1004), the diagram crossfades in place, so "Training distribution" and "Test distribution", and "Coin fixed at end wall" and "Coin randomized", overlap as garbled text for about 0.1 s, while the heading already reads "Test · coin moved". The METHOD and OBSERVED RESULT badges also overlap. These beats are consecutive in the source, so no omitted beat leaks in.
  - [minor] s05b02: For about 0.1 s after the cut (frames 2009-2011), the diagram titles "Decorrelating proxies" and "CoinRun training" overlap ("DeCoinRun trainingies"), and the HYPOTHESIS/OBSERVED RESULT badges overlap. The same overlap occurs at the s05b03 start ("CoinRun training" over "Varied locations").
  - [minor] s03b01: At 360 px width, "Intended: reach coin", "Shortcut: move right" and the purple "Hypothesis: proxy favored by bias" tag are about 6-7 px tall, and the purple tag has low contrast on the dark panel. The hypothesis status is also carried by the heading and the italic caption, so the meaning survives.
  - [minor] s05b01: The diagram labels the proxy "Proxy: reach right wall", while s03b01 shows "Shortcut: move right" and the narration says "rightward progress". In the paper, "move to the wall" is the critic's proxy and "move right" is the policy's (c21), so the label is inconsistent with the rest of the edit.
  - [minor] s06b03: At 360 px, "High training performance" and "Divergent objective" on the balance scale are about 7 px tall, and the grey serif "Performance is not alignment" has low contrast.
  - [minor] s01b01: The epistemic badges (THREAT MODEL, BACKGROUND, METHOD, OBSERVED RESULT, HYPOTHESIS, AUTHORS' INTERPRETATION, STATED LIMITATION) are about 6 px tall at 360 px width throughout the short. They are barely legible, even though they carry the status distinctions.
  - [minor] s01b01: Review limitation: I could not play or listen to the audio. Narration completeness was checked instead. Each segment equals its WAV length plus about 0.35 s of padding, and silencedetect shows every cut inside a silence of 0.3 s or more. Captions were checked against the speech pauses.
- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`.

## Media backups
- No pending entries in `automations/backlog/media-backups.md`.

