# Publish a paper

Turn one AI safety paper into a draft explainer on aisafetyrisks.org: source-grounded notes, a
storyboard, a narrated Manim video, a thumbnail, a web page and a YouTube package. Run it from
start to finish without asking the user anything. The result stops at human review; publication
is the user's decision.

Use this workflow when asked to publish, process or make an explainer for a paper (an arXiv id, a
URL, a PDF, or a paper from `automations/backlog/papers.yaml`), or to resume one.

## What a good explainer is

It makes research easy to understand for a general audience and makes clear why it matters for AI
safety, in the real world, to the viewer. Every video has the same shape:

1. **Opening:** a real-world situation the viewer recognizes, the AI safety risk in it, then what
   the paper asked and did.
2. **Roadmap:** a checklist of 3 to 5 items the video will cover.
3. **Body:** scenes that deliver those items in order. The kit shows the checklist at each new item
   and ticks off the one just finished.
4. **Closing:** the last item ticked, back to the real-world situation, what the paper does not
   show, and one takeaway.

`paper-video check <slug> storyboard` enforces this shape and the kit draws every checkpoint. The
storyboard brief explains each part. Accuracy comes first: every claim about the paper cites notes
whose quotes are verified against the paper. Only step 2 reads the paper; every later step works
from `notes.yaml`.

## How to work

- Run every command from the repository root as `uv run --frozen paper-video ...`. `<slug>` is the
  work's directory name under `automations/works/`, printed by `ingest`.
- A **brief** is a file that `paper-video brief` writes to `automations/works/<slug>/briefs/`. It
  holds the instructions, the inputs, where to write the output and the command that checks it.
  Read it and do exactly what it says.
- Every command fails loudly with a list of problems. Fix each listed problem and run the command
  again.
- **Subagents** are fresh general-purpose agents started with the Agent tool. Give them exactly the
  prompt shown in the step, with `<slug>` and `<id>` filled in.
- After each step, tell the user in one line what finished and what comes next. Do not wait for
  an answer.
- Round limits keep the run cheap. When a limit is reached, keep going and list what is still open
  at handover.
- To resume a work, run `paper-video report <slug>` and start at the first step whose output is
  missing or failing.

## Steps

### 1. Ingest

`paper-video ingest <paper>`. For a local PDF or a bare PDF URL, add `--source-url` with the
paper's public page.

### 2. Notes

`paper-video brief <slug> analyze`. Follow the brief: write `notes.yaml`, then run
`paper-video check <slug> notes` until it passes.

### 3. Storyboard

1. `paper-video brief <slug> storyboard`. Follow the brief: write `storyboard.yaml`, then run
   `paper-video check <slug> storyboard` until it passes.
2. **Audience review**, one round. Start a subagent:
   > Run `uv run --frozen paper-video brief <slug> review-audience` from the repository root,
   > read the brief it writes, and follow it exactly.

   Fix every major issue it reports in `storyboard.yaml` and run the check until it passes.
3. **Science review**, at most 2 rounds. Start a subagent:
   > Run `uv run --frozen paper-video brief <slug> review-storyboard` from the repository root,
   > read the brief it writes, and follow it exactly. Report the output of the final
   > `paper-video review` command.

   If the first review reports blocker or major issues, fix them (see **Fixing**), run the check
   until it passes, and start a new subagent with the same prompt. Do not fix after the second
   review; its open issues go into the handover.

### 4. Narration

`paper-video narrate <slug>`.

### 5. Scenes

1. `paper-video render <slug>`. The first time, it fails and lists every scene, because no scene
   code exists yet.
2. For each scene it lists, start a subagent, at most `parallel_scenes` (in
   `automations/config.toml`) at a time:
   > Run `uv run --frozen paper-video brief <slug> scene --scene <id>` from the repository root,
   > read the brief it writes, and follow it exactly. Report the final render output and anything
   > still wrong.
3. When all have finished, run `paper-video render <slug>`. It must end without an error: every
   scene rendered, with a visual review of its current render. For a scene it still lists, start
   one more subagent with the same prompt. Do not write scene code yourself.

### 6. Video

1. `paper-video assemble <slug>`. If it lists timeline problems (for example a chapter shorter
   than 10 s), fix them in `storyboard.yaml`, run the check, and repeat steps 4 and 5; only the
   scenes that `render` lists need new subagents.
2. Read `out/captions.vtt` from start to finish and check the shape: within about 90 seconds the
   viewer knows the real-world risk and what the paper did; each roadmap item is answered in its
   chapter; the closing returns to the opening's situation. Note any failure for the handover; do
   not start another round.

### 7. Thumbnail

`paper-video brief <slug> thumbnail`. Follow the brief: write `scenes/thumbnail.py` and run
`paper-video thumbnail <slug>` until it passes. Look at `out/thumbnail.jpg` at small size and fix
it if the headline is not readable at a glance or the image does not show what the headline says.

### 8. Web page

1. `paper-video brief <slug> site`. Follow the brief: write `site.yaml` and run
   `paper-video site <slug>` until it passes.
2. **Science review**, at most 2 rounds, as in step 3.3 but with `review-site` in place of
   `review-storyboard`. Fix blocker and major issues from the first review in `site.yaml` and
   re-run `paper-video site <slug>` before the second.

### 9. YouTube

Write `youtube-copy.yaml` following `automations/src/paper_video/prompts/youtube.md`, then run
`paper-video youtube <slug>`.

### 10. Hand over

Run `paper-video report <slug>`, then tell the user:
- where the results are: `automations/works/<slug>/out/video.mp4`, `out/thumbnail.jpg`,
  `youtube.yaml`, and the page, previewed with
  `uv run --frozen aisr-site serve --drafts --media-root automations/media`;
- every open review issue with its severity, every scene with remaining visual problems, and any
  shape failure from step 6.

## Fixing

- Change only what the issue is about, with the smallest edit that fully resolves it. Keep
  everything else, including ids.
- If a fix needs support that the notes do not contain, remove or soften the statement.
- After a storyboard edit, run `paper-video check <slug> storyboard` and `paper-video narrate
  <slug>`. `render` then lists only the scenes whose code must be updated.

## Rules

- Scientific integrity comes first: `automations/src/paper_video/prompts/integrity.md` applies to
  everything written in this workflow.
- Do not edit `automations/kit/`, the `paper-video` code or files under `checks/`. Helpers for one
  video live in its scene files.
- Never run `paper-video approve` or deploy. Approval marks a human review and uploads
  media to production.
