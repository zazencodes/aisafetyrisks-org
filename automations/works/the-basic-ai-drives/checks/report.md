# Review report: the-basic-ai-drives

Standing authorization covers site publication after all required checks pass; no personal review or confirmation is required. Inspect `out/video.mp4` and the page
(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against
the evidence register. Then run `paper-video approve the-basic-ai-drives`.

## Source notes
- Quotes found in the PDF: yes. Page corrections: 0.

## Storyboard
- Provenance checks: pass.
- Science review: **none of the current version**.

## Web page
- Provenance checks: pass.
- Science review: **accurate**.

## Scenes
- s01: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s01-sheet.png`)
  - [minor] s01b03: The end-of-beat contact-sheet frame is empty apart from the heading and citation, because the definition diagram deliberately fades out in the last 0.8 s so that s01b04 opens on its own visual. The full system, drive and counteract diagram is visible for the rest of the beat.
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s02-sheet.png`)
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s03-sheet.png`)
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=0 (contact sheet `frames/s04-sheet.png`)
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s05-sheet.png`)
  - [minor] s05b02: The end-of-beat contact-sheet frame shows only the heading, tag and citation, because the chess and measurement diagram deliberately fades out in the last 0.8 s so that s05b03 opens on its own visual. The real-outcome/measurement diagram is visible for the rest of the beat.
  - [minor] s05b04: The storyboard visual asks for the shutdown control adjacent to the route, but s05b04 omits it because its narration does not mention shutdown and 'Off switch' is not in the beat's on-screen text; s05b03 likewise omits the measurement ring that only s05b02 explains.

## Video
- Duration 502 s, 1920x1080.

## Short-form companion
- Checks pass: 126.60s, 1080x1920, current independent review.
  - [minor] s04b05: The closing clause "unless the system's goals make them matter" (italicized in the caption) is not in the c33 quote, which states without condition that "the pressure to acquire resources does not take account of the negative externalities imposed on others." The qualifier is a reasonable inference from c14 (utility that includes another agent's welfare) and c34 (utility engineering), but here it reads as part of the paper's c33 statement, and the emphasis draws attention to the editorial addition rather than to the paper's point.
  - [minor] s04b01: The caption break puts "Unless designed otherwise, that" on one cue and the bold phrase "can create an incentive for self-preservation" on the next. The condition from c28 ("unless they are explicitly constructed otherwise") is spoken but is not visible beside the emphasized claim.
  - [minor] s05b04: "For the chess machine, safety requires thinking through the route to success" is an editorial takeaway; "requires" is firmer than the paper's c34 proposal ("would go a long way toward"). It is unlikely to mislead because the preceding sentence attributes the proposal to Omohundro.
  - [minor] s05b03: About 1 s after the cut, the "Hypothetical examples" recap frame adds a middle icon (one circle forking into two outlined circles). It comes from omitted beats (the self-modification fork and copies/replication in s02b02 and s04b02) and has no antecedent in this edit. It carries no label, and the chess-to-goal and resources icons do correspond to included beats, so the impact is small. No other label, badge or diagram from an omitted beat was visible at any cut. I checked the first frame and frames +1, +3, +8, +15, +30 and +60 at all seven cuts, including the source skips s01b01->s01b04, s01b04->s04b01, s04b01->s04b04 and s04b05->s05b03.
  - [minor] s05b03: The status badge reads "STATED LIMITATION", but the narration explicitly frames the boundary ("does not measure how often these behaviors occur in deployed artificial intelligence") as editorial context, and the cited claim c03 is a method claim. The badge implies the author stated this caveat.
  - [minor] s05b04: For roughly the first 0.5 s of the takeaway, the s05b03 "STATED LIMITATION" badge stays on screen above the "Examine the route to success" heading. The badge then morphs into "AUTHORS' INTERPRETATION" through a frame or two of overlapping, garbled glyphs. The s04b04->s04b05 badge morph ("AUTHORS' INTERPRETATION" -> "THREAT MODEL", about 1 s after the cut) shows the same overlapping glyphs.
  - [minor] s04b04: The goal box is labelled "Original goal". In the full video this contrasts with the proxy/helper goal from the omitted s04b03, but this edit has no other goal for "original" to contrast with. Earlier in the short, the goal is labelled "Win games" (s01b01) and "Future progress" (s04b01).
  - [minor] s01b01: At 360 px width, the epistemic status badges (e.g. "THREAT MODEL", "AUTHORS' INTERPRETATION") have a cap height of about 4-5 px, and the duplicate in-diagram "OMOHUNDRO (2007)" citation just above the scope label is about 3-4 px and effectively unreadable. The larger citation and scope label below remain readable, so source context is not lost, but the status badge is the only on-screen marker of epistemic status. This applies to all beats. The essential diagram labels (Chess, Win games, Off switch, Future progress, Shutdown, Space/Time/Matter/Free energy, Trade, Taking, Costs to others, Conceptual argument, Hypothetical examples, Design consequences, Route to success, Goal) are readable at 360 px with good contrast.
  - [minor] s04b05: The italic caption shows a visible space before the final period ("make them matter ."), and the same occurs in s01b01 ("chess-playing robot ."). This is a typographic artifact at the italic/roman boundary. Otherwise all caption cues use at most two lines, the same off-white ink throughout, and no clipping; bold and italic remain legible at phone size.
  - [minor] s01b01: Review limitation: I could not listen to the audio. Instead, I verified narration completeness by comparing the selected WAV durations (15.20, 18.96, 17.52, 19.52, 19.12, 16.88, 16.96 s) with the segment durations (each about 0.35 s longer) and by running silence detection on the MP4. Every cut (15.57, 34.87, 52.73, 72.60, 92.07, 109.30 s) falls inside a silence, and speech ends at 126.17 s of 126.6 s, so no words appear to be cut. Burned-caption cues stay within about 0.4 s of the speech pauses.
- Video: `out/short/video.mp4`; social copy and links: `short-package.yaml`.

## Media backups
- No pending entries in `automations/backlog/media-backups.md`.

