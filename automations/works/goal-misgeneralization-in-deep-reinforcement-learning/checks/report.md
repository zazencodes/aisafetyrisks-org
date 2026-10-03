# Review report: goal-misgeneralization-in-deep-reinforcement-learning

Human review is required before publication. Watch `out/video.mp4` in full, read the page
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
- s01: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s01-sheet.png`)
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s02-sheet.png`)
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s03-sheet.png`)
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s04-sheet.png`)
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s05-sheet.png`)
- s06: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s06-sheet.png`)

## Video
- Duration 257 s, 1920x1080.

## Short-form companion
- Checks pass: 114.20s, 1080x1920, current independent review.
  - [minor] s05b03.on_screen_text: The inherited diagram says 'Shortcut broken', although c14 supports improved goal generalization with 2% randomized training levels and further improvement with more randomization. The narration and portrait heading correctly describe weakening the shortcut, which limits the misleading implication of that stronger diagram label.
  - [minor] s03b01: At 360x640 phone size, auxiliary diagram labels such as 'Always co-occur', 'Visual object tracking', 'Simpler directional cue' and the inductive-bias hypothesis are very small and low contrast. Some comparison and scope-boundary labels in s05b02 and s06b02 are similarly difficult to read. Their essential meanings remain in the legible narration captions and portrait headings; no essential experimental condition relies solely on the small labels.
  - [minor] s01b03: This cut briefly inherits the capability-failure/risk comparison from the omitted preceding source beat before the study card replaces it. The label 'Risk: arbitrarily bad states' remains during the early transition. s06b02 similarly begins with the omitted deployment-threat-model diagram before transitioning to scope boundaries. These are labelled source visuals, but the selected beat claim lists omit the additional inherited threat-model claims.
  - [minor] s01b01: Continuous playback and listening were unavailable. I reviewed the entire supplied brief against the verified notes, the contact sheet, full-resolution individual frames, and additional actual-video frames at 360px phone size covering caption colors, CoinRun cuts and limitations. All 41 rendered ASS cues have at most two lines and one accent color; highlighted phrases preserve their meaning. Every selected WAV fits within its segment with 0.34-0.37 seconds padding. Caption timing relative to heard speech was not verified.
- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`.

