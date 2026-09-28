# Review report: concrete-problems-in-ai-safety

Human review is required before publication. Watch `out/video.mp4` in full, read the page
(`uv run aisr-site serve --drafts --media-root automations/media`), and check each claim against
the evidence register. Then run `paper-video approve concrete-problems-in-ai-safety`.

## Source notes
- Quotes found in the PDF: yes. Page corrections: 0.

## Storyboard
- Provenance checks: pass.
- Science review: **none of the current version**.

## Web page
- Provenance checks: pass.
- Science review: **needs_revision**.
  - [major] explanation[4]: "Hard-coded rules against disasters work well when only a few things could go wrong and designers know them all [c39]" keeps only the condition and drops the authors' conclusion in c39: as agents become more autonomous in complex domains (such as running a power grid), hard-coding every failure is unlikely to be feasible, so a principled approach seems essential. As written, a non-expert can read it as an endorsement of hard-coding as the fix for unsafe exploration, which is the opposite of the paper's point.
  - [minor] explanation[4]: Exploration is described only as "trying actions whose effects they do not yet know [c38]"; the reason it is a safety problem in c38 (it can be dangerous; badly chosen actions may destroy the agent or trap it in states it cannot get out of, unlike bounded harm in toy environments like Atari) is left implicit.
  - [minor] summary: "calls its ideas preliminary [c14]" applies c14 to all of the paper's ideas, but c14 says this of the avenues for the wrong-objective problems (reward hacking, side effects, and to a lesser extent scalable supervision), where less prior work exists. limitations[0] states this correctly.
  - [minor] explanation[1]: "A penalty for the vase would not help with the many other things it could disturb" is stronger than c15, which says it may not be feasible to identify and penalize every possible disruption ("many different kinds of 'vase'").
  - [minor] explanation[0]: The opening scene combines the paper's side-effect (vase) and reward-hacking (unseen messes) examples into one composite scenario with no claim id, then says "The authors see small accidents like this as a concrete threat [c45]". c45 is about small-scale accidents given ML controlling industrial and health-related systems, not about this composite office scene.
  - [minor] explanation[3]: "The best measure of a clean office is a person inspecting it for hours" paraphrases c34 loosely: the objective in c34 is "how happy would the user be after hours of inspecting the result", not the inspection itself.
  - [minor] findings[3]: The call for a unified approach is stated without its stated basis: the authors tie it to the increasing trend towards end-to-end, fully autonomous systems (c45). The finding also omits that the authors say the risk of larger accidents is harder to gauge.
  - [minor] findings[0]: The finding is labelled "definition", but the claim it cites, c02, is of kind "method" (the paper's categorization of problems).
  - [minor] context: "Its value is the framing" is an editorial judgment presented without attribution, and "practical design problems with objectives, oversight and training data" drops the "insufficiently expressive model" cause in c10.

## Scenes
- s01: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s01-sheet.png`)
  - [minor] s01b03: After the office shrinks to make room for the Industry and Health care panels, "Score looks good" and "Room is not" are scaled down to about size 22, smaller than the panel labels.
- s02: rendered=True, layout problems=0, visual review=recorded, visual issues=1 (contact sheet `frames/s02-sheet.png`)
  - [minor] s02b01: The shrunken office in the lower right is small, so the messes and score counter read only as specks.
- s03: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s03-sheet.png`)
  - [minor] s03b01: The knocked vase is a small red ellipse and reads weakly as a toppled vase.
  - [minor] s03b04: The target mark draws over the delivered box, so the box looks translucent on the target.
- s04: rendered=True, layout problems=0, visual review=recorded, visual issues=3 (contact sheet `frames/s04-sheet.png`)
  - [minor] s04b05: In the game screen the player square ends touching the flag, so the two are hard to tell apart in the final frame.
  - [minor] s04b06: The "Trip wire" label sits in the right-hand column, far from the red line in the doorway it names.
  - [minor] s04b06: The frozen robot is grey but its white eye is still open, which weakens the "stopped" reading.
- s05: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s05-sheet.png`)
  - [minor] s05b03: The faint gold estimates above the hidden runs are close in tone to the revealed scores, so seen and estimated scores separate mainly by the square fill.
  - [minor] s05b02: The robot, mess and rug sit in the right half of the office, leaving the left half of the floor empty.
- s06: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s06-sheet.png`)
  - [minor] s06b02: The red "no" markers on the power grid cluster in the left half, so the grid reads as unevenly marked rather than sparsely marked everywhere.
  - [minor] s06b03: In the simulation panel the outlet trial path and the middle trial path run close together near the robot and partly overlap.
- s07: rendered=True, layout problems=0, visual review=recorded, visual issues=2 (contact sheet `frames/s07-sheet.png`)
  - [minor] s07b04: "Knows when it is wrong" fills its box almost edge to edge, leaving little padding.
  - [minor] s07b01: After the robot leaves, the training office holds only four mess dots and looks sparse next to the busy factory.
- s08: rendered=True, layout problems=0, visual review=recorded, visual issues=3 (contact sheet `frames/s08-sheet.png`)
  - [minor] s08b01: The "Reward hacking" tab sits on the office floor's top edge, so its border touches the floor outline.
  - [minor] s08b02: The office panel has no label, while the factory and hospital panels are labelled "Industrial" and "Health".
  - [minor] s08b03: The five tabs are laid out in two rows (three and two) rather than one row, to keep them legible at full size.

## Video
- Duration 472 s, 1920x1080.

