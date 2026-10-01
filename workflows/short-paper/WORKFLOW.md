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
2. **Build.** Run `paper-video short <slug>`. Fix every failure and repeat until it produces
   `out/short/video.mp4`, `out/short/cover.jpg`, captions in SRT/VTT, `out/short/timeline.json`,
   `frames/short-sheet.png`, and `short-package.yaml`. It checks source provenance and current
   renders, preserves complete narration, burns portrait captions, and refuses runtimes of 180
   seconds or more. Paid narration is reused; no LLM call is made by the command.
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
   When manually uploading to YouTube, associate it with the full video through the related-video
   control when the full video has a YouTube URL. Nothing in this workflow uploads or posts.

## Rules

- Follow `automations/src/paper_video/prompts/integrity.md`. Shorter explanations retain epistemic
  status, conditions and caveats. The independent review covers new headings and social copy too.
- Exactly one canonical edit: `short.yaml`. Outputs live in `out/short/`; reruns replace that draft.
  Cache keys make interrupted builds resumable and refuse stale reviews after inputs change.
- A selected beat can rely on diagrams established earlier in its scene. Inspect each new cut;
  include the setup if an isolated cut fails to explain itself. If a suitable edit cannot be made
  from complete beats, improve the source explainer through its workflow and regenerate it first.
- Keep scientific/source and short review artifacts versioned. Binaries remain in the existing
  ignored out/render/frames folders. Do not modify the existing site's publication state for backfills.
- Never run `paper-video approve`, deploy, upload, or post in this workflow. The short is a draft
  until the user reviews it. Paper approval requires a current short with passing independent review;
  approval uploads the long video through the existing publication command, not the social short.
