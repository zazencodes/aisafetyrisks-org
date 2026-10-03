# Review report: frontier-models-are-capable-of-in-context-scheming

Standing authorization covers site publication after all required checks pass; no personal review or confirmation is required. Inspect `out/video.mp4` and the page
(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against
the evidence register. Then run `paper-video approve frontier-models-are-capable-of-in-context-scheming`.

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
  - [minor] s01b05: The Files and Tools labels sit level with the larger Constructed tests label inside the enclosure, so the top row reads slightly crowded.
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s02-sheet.png`)
  - [minor] s02b02: The in-context bracket, labels, information arrow and enclosure fade out during the beat's final 0.4 s, so the end-of-beat frame no longer shows the definition diagram.
  - [minor] s02b05: The Llama 3.1, Claude 3 Opus and o1 labels sit just below the enclosure, close to the source note row.
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s03-sheet.png`)
  - [minor] s03b02: The returned/expected comparison and Explanation card fade out during the beat's final 0.4 s, so the end-of-beat frame shows only the pipeline.
  - [minor] s03b04: The short connector arrows in the stacked pipeline column are small at phone width, though the four labelled boxes read as the same pipeline in order.
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s04-sheet.png`)
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s05-sheet.png`)
  - [minor] s05b01: The connector arrows between the four pipeline boxes are short, so the flow direction reads mainly from box order.

## Video
- Duration 434 s, 1920x1080.

## Short-form companion
- Checks pass: 159.60s, 1080x1920, current independent review.
  - [minor] s05b04: The takeaway ("trace how an agent produced an answer, as well as reading the answer itself") is shown under an "AUTHORS' INTERPRETATION" badge, but it is the edit's own takeaway. The nearest authors' statement is the recommendation of automated CoT monitoring and explicit safety arguments (c35), which is narrower than general process tracing. The cited claims (c21, c38) are results, not this recommendation.
  - [minor] title: "How an AI agent can quietly alter a ranking" puts "quietly" on the agent's behaviour in general. The notes support covert behaviour in the hypothetical hook and the authors' interpretation of scheming against the user (c21), but give no observed result on whether o1 concealed or explained the discrepancies (c11 describes the check, not its outcome). The on-screen scope label limits the setting, so this is unlikely to mislead badly.
  - [minor] s05b03: At the exact cut from s03b06 (124.667 s) the panel jumps from the 22% chart to a "Back to the inbox" panel with an "Agent" and a "Conflicting goal" arrow into "Input data". That state comes from omitted s05b01 ("Return to that hypothetical inbox assistant") and is not narrated in this edit. About 2 s later the same pipeline is boxed as "Constructed evidence". Putting the hypothetical inbox title over a box labelled as evidence slightly blurs the illustrative scenario and the experiment. The narration states the limitation clearly, and the pipeline labels match the s03 evaluation workflow, so nothing is contradicted.
  - [minor] s03b04: The 22% value lags the speech. The caption "o1 produced false rankings in 22% of rollouts" runs from about 99.2 to 102.5 s, but the bar only starts at about 103 s and the "22%" label appears at about 105 s. The bar height matches 22% on the zero-based 0-100% axis.
  - [minor] s03b04: The purple bracket captioned "Authors' interpretation" encloses the "Changed input" and "Replaced ranking" markers. Those actions are observed results (c38); only the reading of them as scheming against the user is the authors' interpretation (c21). A viewer could take the actions themselves as interpretation.
  - [minor] s05b04: The moving trace dot passes over the box labels ("Emails", "Input data", "Scoring code", "Scores") and covers a character for a few frames, e.g. "Sc*res" at about 150 s. The labels stay readable otherwise.
  - [minor] s01b04: The s01 panel title "A plausible list", which belongs to the hypothetical hook, stays above the METHOD-badged "Constructed tests" diagram. The panel badge changes from FUTURE SCENARIO to METHOD at the cut, so status is still signalled, but the title still refers to the hypothetical.
  - [minor] s03b04: Readability at 360 px is marginal for small text. The epistemic-status badges (OBSERVED RESULT, AUTHORS' INTERPRETATION, STATED LIMITATION) are about 5 px tall. Secondary labels in s03b04 and s05b03/s05b04 ("Replaced ranking", "Situation memo", "Human goal", "Conflicting goal", "Deployment remains open") are about 7-8 px. The in-panel citation "Meinke et al. (2024)" is tiny, though it is duplicated legibly below. Essential values ("22%", "o1", "Strong goal nudge", "Pre-deployment o1") and all captions and headings are readable with good contrast.
  - [minor] s01b01: Review limitation: audio playback was not available. Narration completeness was checked by comparing the WAV lengths with the timeline. Every segment is 0.27-0.48 s longer than its WAV, and the final WAV ends at about 159.17 s, within the 159.6 s audio stream. Captions, which use the same off-white ink and show at most two lines, were also checked against the narration. No cut words were found, but none were heard.
- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`.

## Media backups
- No pending entries in `automations/backlog/media-backups.md`.

