# Make one short-form paper explainer

Make exactly one 1080x1920, 30 fps short from a completed long-form explainer. Its runtime must be
strictly less than three minutes. Produce a reviewable draft and a social package; stop before
posting. Use this workflow after full-video assembly in publish-paper, or to backfill an existing
published explainer. This workflow may change short-related pipeline code when explicitly asked
to implement or fix the workflow.

## Order and inputs

For backfills, sort the published entries of `automations/backlog/papers.yaml` by the paper's
`published` date ascending (the research date, not the site publication date). Start with the first
one whose current short does not pass `paper-video check <slug> short`. Handle one paper per
session unless the user asks for a batch. Generating a short never changes a published site's
page, publication timestamps, long video, or backlog publication status.

Run commands from the repository root as `uv run --frozen paper-video ...`. Use the paper's
existing source-verified `notes.yaml`, completed storyboard, cached narration, and scene renders.
Choose the edit after the full video is assembled: reuse whole beats and redraw the portrait
headings/captions around the complete landscape diagrams. This preserves the original animations,
voice and claim provenance without another narration bill. Do not blindly center-crop diagrams.

## Steps

1. **Choose the edit.** Run `paper-video brief <slug> short` and read the entire brief. Inspect the
   completed video's storyboard, captions and scene frames. Write `short.yaml`: one hook, context,
   explanation, a spoken limitation, and a takeaway. Prefer 90–150 seconds, leaving room below the
   hard limit. Read the selected narration in order and check every antecedent and retained condition.
   **Choose caption emphasis separately from the edit.** Read the complete selected narration,
   then choose sparse exact phrases: bold for the main mechanism, contrast or takeaway; italic
   for necessary qualifications and evidence boundaries. Keep all caption text off-white.
   Include meaning-bearing negations and conditions. Leave routine dates, names and context
   plain; `caption_emphasis: []` is encouraged. Review the phrase list across the whole short
   before building, using the selection rules in `automations/src/paper_video/prompts/short.md`.
2. **Build.** Run `paper-video short <slug>`. Fix every failure and repeat until it produces
   `out/short/video.mp4`, `out/short/cover.jpg`, captions in SRT/VTT, `out/short/timeline.json`,
   `frames/short-sheet.png`, and `short-package.yaml`. It checks source provenance and current
   renders, preserves complete narration, burns portrait captions, and refuses runtimes of 180
   seconds or more. Paid narration is reused; no LLM call is made by the command.
   The command also automatically archives the completed exports, narration and available edit
   metadata to the approved Expansion drive location in AGENTS.md and `automations/config.toml`.
   It logs the verified snapshot path. No confirmation is needed for this backup. A missing drive
   or failed backup records a deferred paper/export row in `automations/backlog/media-backups.md`
   while retaining local exports and narration. Say the backup will be updated later and continue
   all short checks; do not block or ask the user to connect the drive. Retry with
   `uv run --frozen paper-video backup-pending` when the drive is available. See
   [the backup guide](../../docs/media-backup-plan.md).
3. **Independent science and visual review**, at most two rounds. Start a fresh subagent:
   > Run `uv run --frozen paper-video brief <slug> review-short` from the repository root, read
   > the brief it writes, and follow it exactly. Inspect the rendered frames and actual edit for
   > scientific accuracy and mobile readability. Write short-review.yaml and report the final
   > `paper-video check <slug> short` output. Do not edit the plan or pipeline.

   Fix every blocker or major issue in the first review. Rebuild the short and start a fresh
   reviewer. Any source, plan, narration or renderer change invalidates the old review. If the
   second review still fails, hand over the issues and mark the short incomplete; do not claim
   completion. Minor issues must be listed at handover.
4. **Package and hand over.** Run `paper-video check <slug> short`, then `paper-video short <slug>`
   to refresh the package with the recorded review, and `paper-video report <slug>`. Link the short,
   cover, captions and social package. State its actual duration and every open review issue.
   `short-package.yaml` contains draft copy, the paper citation, full explainer URL and paper URL.
   Nothing in this workflow uploads or posts; the short is posted with its long-form video by
   [the scheduling workflow](../schedule-posts/WORKFLOW.md).

## Rules

- Follow `automations/src/paper_video/prompts/integrity.md`. Shorter explanations retain epistemic
  status, conditions and caveats. The independent review covers new headings and social copy too.
- Exactly one canonical edit: `short.yaml`. Outputs live in `out/short/`; reruns replace that draft.
  Cache keys make interrupted builds resumable and refuse stale reviews after inputs change.
- Every selected beat must have a self-contained visual opening from its first frame. Inspect
  the exact cut and the following transition at phone size: labels or diagrams from omitted beats
  must not appear without explanation. Clear obsolete state and establish the necessary diagram
  in the source scene before the selected beat starts; retain its complete narration. Include the
  setup if the diagram genuinely depends on it. Essential labels must be readable at 360-pixel
  phone width with sufficient contrast; enlarge and reflow them, or remove redundant secondary
  text already explained by narration. Verify box counts, chart labels and values against notes.
  Text never morphs into other text or overlaps mid-swap, at cuts or inside beats; diagrams never
  say more than the narration. `frames/short-sheet.png` shows every cut's first frame and transition
  at phone width; check it yourself before starting a review round, so reviews find little.
  Improve the source explainer through its workflow and regenerate affected scenes and videos.
- Captions follow word timings that local whisper.cpp reads from the cached narration WAVs
  (`[captions]` in `automations/config.toml`). Never regenerate narration to fix caption timing.
- Keep scientific/source and short review artifacts versioned. Binaries remain in the existing
  ignored out/render/frames folders. Do not modify the existing site's publication state for backfills.
- This workflow produces the local short and package; posting follows the scheduling workflow
  only when the user asks for it. When used as the companion step in publish-paper, return to that workflow to
  approve and deploy the full explainer under standing authorization after all checks pass.
  Standalone short backfills do not approve or redeploy the existing site. Paper approval requires
  a current short with passing independent review and uploads the long video, not the social short.
