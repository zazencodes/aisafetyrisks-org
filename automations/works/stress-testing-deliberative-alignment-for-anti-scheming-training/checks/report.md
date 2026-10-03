# Review report: stress-testing-deliberative-alignment-for-anti-scheming-training

Standing authorization covers site publication after all required checks pass; no personal review or confirmation is required. Inspect `out/video.mp4` and the page
(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against
the evidence register. Then run `paper-video approve stress-testing-deliberative-alignment-for-anti-scheming-training`.

## Source notes
- Quotes found in the PDF: yes. Page corrections: 0.

## Storyboard
- Provenance checks: pass.
- Science review: **accurate**.

## Web page
- Provenance checks: pass.
- Science review: **accurate**.

## Scenes
- s01: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s01-sheet.png`)
  - [minor] s01b03: The end-of-beat frame is nearly empty because the scheming diagram fades out in the last 0.7 s so that s01b04 opens on its own state (required for the portrait short, which cuts from s01b01 to s01b04).
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s02-sheet.png`)
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s03-sheet.png`)
  - [minor] s03b03: The inset model label "o3" sits close to the 13.0% value label after the chart shrinks; they do not overlap and remain readable at 360 px.
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s04-sheet.png`)
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s05-sheet.png`)
- s06: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s06-sheet.png`)
  - [minor] s06b01: The end-of-beat frame is nearly empty because the report diagram fades out in the last 0.7 s so that s06b02 opens on its own state (the portrait short cuts from s03b03 to s06b02).
  - [minor] s06b03: The end-of-beat frame is nearly empty because the proxy diagram and its tag fade out in the last 0.7 s so that s06b04 opens on its own state (the portrait short cuts from s06b02 to s06b04).

## Video
- Duration 546 s, 1920x1080.

## Short-form companion
- Checks pass: 138.30s, 1080x1920, current independent review.
  - [minor] s01b05: The beat says the anti-scheming training was "applied to the finished models" but drops the authors' caveat that doing so likely overestimates the intervention's effectiveness, because it avoids competing pressures from the rest of the training pipeline (c10). The later numbers are correctly bounded to "these tests", so this does not create an overstatement, but the viewer loses the authors' own reason to read 8.7% to 0.3% and 13.0% to 0.4% as a favourable setting.
  - [minor] s01b01 / s06b04: The hook sets up a tidy report that could hide skipped work, but the edit omits the authors' warning (c04, beat s01b03/s06b01) that eliminating visible misbehavior and teaching a model to hide it better can look alike. The takeaway's "keep asking what changed" gestures at it without saying why, so a viewer could read the lower covert action rate as proof that the behavior is gone rather than less observed.
  - [minor] s06b04: "whether recognizing the test helped" has no antecedent in this edit; evaluation awareness (c23-c29) is never introduced, so a viewer does not know models can recognize tests or that the paper examined it.
  - [minor] title: "hidden shortcuts" narrows covert actions, which the paper defines as strategic withholding, misrepresentation or concealment across reward hacking, sabotage, sandbagging and strategic deception (c06, c11). The narration uses the correct definition, so this is unlikely to mislead, but the title implies only skipped work.
  - [minor] s06b04 (badge): The takeaway carries an "AUTHORS' INTERPRETATION" badge, but its content is an observed result (reduction with residual failures, c16, c21) plus the edit's own framing questions, not an interpretation the authors state.
  - [minor] s03b02: The exact first frame at 70.0 s shows the o3 chart with the "13.0%" label but the Before bar still at the o4-mini 8.7% height inherited from the source transform; the bar grows to its correct height over about 0.5 s. The value and bar briefly disagree. No other omitted-beat state appears at this cut.
  - [minor] s06b04: The "Reduced covert actions" diagram shows two tall orange bars with no model names, no Before/After labels and no values; only the tiny post-training marks are labelled "Residual failures". At phone size the dominant orange bars under the heading "Reduced covert actions" can read as high current rates. Heights are roughly proportional to 8.7% and 13.0%, so it does not contradict the narration.
  - [minor] s01b04: While the narration describes the training method, the diagram box is titled "Constructed evaluations", which blurs training environments and test evaluations.
  - [minor] s01b01: At 360 px wide, the status badges (FUTURE SCENARIO, METHOD, OBSERVED RESULT, STATED LIMITATION, AUTHORS' INTERPRETATION) and the in-diagram "Schoen et al. (2025)" credit are about 5 px tall and barely legible; this applies to every beat. Essential diagram labels, chart values (8.7%, 0.3%, 13.0%, 0.4%), the exclusion list and captions are readable with good contrast.
  - [minor] s03b02: Proportional caption timing runs ahead of speech: "The direction is consistent across the models" appears at 74.35 s while the spoken sentence about 13.0% to 0.4% ends near 76.4 s (about 2 s early). In s03b01, "These are rates within the study's evaluations" appears about 1 s before speech reaches it. Other cue starts line up with pauses.
  - [minor] s06b04: Review limitation: the audio could not be listened to. Completeness was checked indirectly; every segment is longer than its WAV (for example s03b01 19.23 s vs 18.88 s), and silencedetect shows a pause spanning each of the 7 cuts, so no words appear clipped.
- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`.

## Media backups
- No pending entries in `automations/backlog/media-backups.md`.

