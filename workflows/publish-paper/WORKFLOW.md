# Publish a paper

Turn one AI safety paper into a draft explainer on aisafetyrisks.org: source-grounded notes, a
storyboard, a narrated Manim video with captions and chapters, a thumbnail, a web page with an
evidence register, and a YouTube package. The result stops at human review; publication is the
user's decision.

Use this workflow when asked to publish, process or make an explainer for a paper (an arXiv id, a
URL, a PDF, or a paper from `automations/backlog/papers.yaml`), or to resume one that stopped.

## Who does what

- **You** (the session running this workflow) write the reading notes, the storyboard, the
  thumbnail scene, the web page draft and the YouTube copy, review rendered contact sheets,
  and apply revisions.
- **Subagents** (general-purpose, started with the Agent tool) do the work that must be
  independent or would flood your context:
  - one subagent per scene writes and renders that scene's Manim code;
  - a fresh subagent does each science review, so the reviewer is never the author.
- **agy** (through the Antigravity CLI, configured under `[agy]` in
  `automations/config.toml`) is called only when an ingested PDF carries no metadata.
- **`paper-video` commands** do everything deterministic: fetching, provenance checks, narration,
  local Manim rendering, assembly, page building. Every command fails loudly with a list of
  problems.

Never use `claude -p` or an LLM API from the pipeline.

Run every command from the repository root as `uv run --frozen paper-video ...`. `<slug>` is the
work's directory name under `automations/works/`.

## Before you start

- `uv sync` has installed Manim Community in the workspace environment.
- For a PDF without metadata, `agy` is on the PATH and logged in.

## Steps

Each step names its inputs and the command that checks its output. When a step is already done
and its check passes, move on. To resume a work, run `paper-video report <slug>` and start at the
first step whose check fails or whose output is missing. **Feedback on a finished draft is a
revision, even when every check passes.** In that case, begin with the revision intake below.

### Revision intake: preserve the working draft

Before changing a storyboard, narration, scene, video, thumbnail, page, or package:

1. Read the user's full feedback and the previous editorial decisions. Inspect the current video
   with its captions from beginning to end, the storyboard, notes, review report, and scene contact
   sheets. Record concrete timecodes and scene ids. A passing provenance or layout check does not
   establish that the explanation works for its audience.
2. Write `editorial-brief.md` with a **revision contract**. Include all active user instructions
   and feedback across the conversation, not just the latest message. Make an acceptance table with
   the requirement, existing timecode or scene, keep/change/remove decision, proposed beat id, and
   how to verify it in the finished video. Fill the proposed beat ids after drafting the new scene
   order. Inventory the existing opening, checklist or roadmap, examples, animations,
   transitions, ending, and any element the user praised or asked to retain. For each one, say
   **keep**, **change**, or **remove**, with a reason grounded in the feedback. Treat useful existing
   animation and structure as assets. If the user says an element failed to solve a problem, improve
   what surrounds it; that statement alone does not authorize removing the element.
3. Draft the new narration and scene order against that inventory. Check the opening separately for
   both jobs: it tells a newcomer what the video is about and why it matters, then gives them a
   concise route through the explanation. Preserve an existing opening checklist unless the user
   explicitly asks to remove it. Put that orientation before the detailed experiment, and make the
   following scenes deliver what it promises.
4. Compare old and proposed storyboards scene by scene. Mark which existing animations and scene
   code can be reused, which need a targeted change, and which genuinely need replacement. A
   revision must not silently turn a developed animation into a static diagram or remove an
   established beat. If a replacement is necessary, document the lost affordance and how the new
   visual serves the same teaching purpose.
5. **Stop before narration or rendering until the contract passes:** every acceptance criterion has
   a planned beat, every keep item is present, the opening has both introduction and orientation,
   and every removal has an explicit reason. Resolve gaps yourself from the source material and
   feedback. Ask the user only if two requirements genuinely conflict or a necessary decision
   cannot be inferred.

This intake is an editorial gate. It comes before expensive audio or video work; do not use a
full render to discover that the planned story dropped a requirement.

### 1. Ingest

`paper-video ingest <paper>`. For a local PDF or bare PDF URL, pass `--source-url` with the
paper's public page. This creates `automations/works/<slug>/` and marks the backlog entry
in progress.

### 2. Reading notes

1. `paper-video brief <slug> analyze`, then read the brief it wrote to `briefs/analyze.md`. It
   holds the full paper text.
2. Write `notes.yaml` as the brief instructs.
3. `paper-video check <slug> notes`. Fix every quote it cannot find in the paper, then re-run it
   until it passes.

### 3. Storyboard

1. `paper-video brief <slug> storyboard`, then read it. For a new paper, write
   `automations/works/<slug>/editorial-brief.md` with these headings: Audience promise;
   Takeaways (at most three); Opening and orientation; Primary experiment; Narrative arc;
   Keep and cut; AI safety relevance; Evidence boundary. For a revision, update that brief
   with the revision contract above. Make editorial decisions from the paper, notes, and user
   feedback. The brief is an authoring artifact, not evidence; paper claims still cite notes ids
   in the storyboard.
2. Write `storyboard.yaml` from the brief. Introduce the subject and its stakes in plain language
   before detailed setup. Use the opening checklist or roadmap to orient viewers, then make each
   section answer a question raised by the previous one. Retain useful experiments and animation;
   compress detail that does not serve the audience promise. Label every real-world bridge as an
   analogy, hypothetical scenario, threat model, or separately sourced case.
3. `paper-video check <slug> storyboard` until it passes.
4. Do an **editorial table read before synthesizing narration**: read only the spoken lines in
   order while looking at the planned visuals and chapter headings. Check the first minute, the
   transitions, and the ending against `editorial-brief.md`. For a revision, verify every
   acceptance criterion and every keep item against exact beat ids. Fix omissions now; a
   provenance check cannot catch them.
   Then have a fresh editorial reviewer compare the brief, previous storyboard, user feedback,
   and proposed storyboard. Ask it to report missing requirements, unjustified removals, weak
   orientation, and lost visual teaching value with exact beat ids. If subagents are disallowed,
   do this as a separate explicit pass in the main session and record that it was self-reviewed.
   Resolve every major issue before narration or rendering; this review does not replace the
   source-grounded science review.
5. Science review: start a fresh subagent with this prompt, filling in the slug:
   > Run `uv run --frozen paper-video brief <slug> review-storyboard` from the
   > repository root, read the brief it writes, and follow it exactly. Report
   > the output of the final `paper-video review` command.
6. If the review lists blocker or major issues, revise (see **Revising** below), re-run the check,
   and review again with a new subagent. Allow at most 2 revision rounds. If blocker or major
   issues remain after that, stop and tell the user.

### 4. Narration

`paper-video narrate <slug>`. It checks the storyboard again, synthesizes narration for any
beat whose text changed, and writes the render context. Re-run it after every storyboard change.

### 5. Scenes

1. On revisions, reuse the current scene code and visual language wherever the editorial brief
   marks them **keep**. Revise only affected scenes. Do not create a new shared visual system or
   replace working animations merely to simplify implementation.
2. `paper-video render <slug>` once. It renders current code and writes contact sheets to
   `frames/<scene>-sheet.png`. A missing visual review is reported as pending.
3. For each scene that needs work, `paper-video brief <slug> scene --scene <id>`, then start a
   subagent:
   > Run `uv run --frozen paper-video brief <slug> scene --scene <id>` from the
   > repository root, read the brief it writes, and follow it exactly: write
   > the scene file, render it, inspect the contact sheet, write the keyed visual review to
   > `visual-reviews/<id>.yaml`, and fix problems until it is clean or you reach the round limit.
   > Report the final render output and anything still wrong.

   Run at most `[render] parallel_scenes` of these subagents at once; each render uses the CPU and
   memory limits in `[render]`.
4. When all have finished, inspect each current contact sheet, write or update its keyed review in
   `visual-reviews/<scene>.yaml`, then run `paper-video render <slug>` again. Unchanged scenes come
   from the cache. Every scene must render and have a review of its current render. Report any scene that still has
   layout problems or blocker/major visual issues.

### 6. Video

`paper-video assemble <slug>`. It refuses renders that are out of date with their code or
narration. It writes `out/video.mp4`, captions and the chapter timeline, and lists any timeline
problems (for example chapters shorter than 10 s). Fix those in the storyboard and go back to step 4.

### 7. Thumbnail

`paper-video brief <slug> thumbnail`, read it, write `scenes/thumbnail.py`, then run
`paper-video thumbnail <slug>` until it passes. Look at `out/thumbnail.jpg` and improve it if it
does not read clearly at small sizes.

### 8. Web page

1. `paper-video brief <slug> site`, read it, write `site.yaml`.
2. `paper-video site <slug>` until it passes. It checks provenance and writes
   `site/content/works/<slug>/`.
3. Do a science review as in step 3, using the task `review-site` and the subject `site`. Revise
   `site.yaml` and re-run `paper-video site` for blocker or major issues, at most 2 rounds.

### 9. YouTube

Write `youtube-copy.yaml` with `title`, `description` and `tags` according to
`automations/src/paper_video/prompts/youtube.md`. Then `paper-video youtube <slug>` writes
`youtube.yaml`. Read the packaged title and description and correct anything that misstates the notes.

### 10. Hand over

`paper-video report <slug>`, then tell the user:
- what was produced and where (`out/video.mp4`, the page, `youtube.yaml`);
- every science review issue still open, with its severity;
- every scene with remaining layout or visual issues;
- anything you changed by hand, and why.

Before handoff, watch the assembled video with its captions from beginning to end. Compare it to
`editorial-brief.md`, not just the provenance and layout reports. On revisions, check every
acceptance criterion and keep item at its actual timecode, including the opening introduction and
checklist. Check that retained animations still communicate their intended mechanism, that
transitions advance the audience question, and that the ending returns to the promise with the
evidence boundary intact. Revise only affected material if this pass finds a major problem, then
repeat the necessary checks and assembly.

Do not run `paper-video approve` and do not deploy. Approval records a named human reviewer and
uploads media to production.

## Revising

- Fix every listed blocker and major issue with the smallest change that fully resolves it. Keep
  everything else, including ids.
- If a fix needs support that the notes do not contain, remove or soften the statement. Do not
  invent support. If the notes themselves are wrong, fix `notes.yaml` against the paper and re-run
  its check.
- Any edit to the storyboard or the page after a review makes that review stale. `approve` accepts
  only a review of the current content, so review again after edits.
- A storyboard edit changes the hashes of the scenes it touches. Re-run `narrate`, then regenerate
  only the scenes that `render` now rejects.

## Rules

- Scientific integrity comes first. The rules in `automations/src/paper_video/prompts/integrity.md`
  apply to everything you write.
- Never edit files under `checks/` by hand. Only commands and reviewers write there.
- Keep the user informed: after each step, say in one line what finished and what comes next.
