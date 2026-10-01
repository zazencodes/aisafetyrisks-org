# aisafetyrisks.org

An educational site that explains AI safety research through animated explainers (Manim
Community), with every claim traced to a quote in the source paper. It is a `uv` workspace with
two packages:

- `site/`: static site generator (`aisr-site`) deployed to Cloudflare Workers static assets.
  Content lives in `site/content/`; output goes to `site/dist/`.
- `automations/`: `paper-video`, the deterministic steps of turning a paper into an explainer
  (ingest, provenance checks, ElevenLabs v4 narration, local Manim rendering, assembly, page and YouTube
  packaging). Configuration is in `automations/config.toml`, and every key is required. Per-paper
  work directories are in `automations/works/<slug>/`.

## Usage

The main way to run this project is to work through the research backlog,
`automations/backlog/papers.yaml`, one paper per agent session, oldest first. Start a session with:

> Read `automations/backlog/papers.yaml` and follow the instructions at the top: take the first
> `queued` paper and run `workflows/publish-paper/WORKFLOW.md` for it.

Each paper's `status` in that file tracks its progress. The user reviews each draft and approves it
with `paper-video approve <slug>`.

## Workflows

Workflows are step-by-step procedures for agents, in `workflows/<name>/WORKFLOW.md`. When a task
matches one, read the whole file before starting and follow it.

- `workflows/publish-paper/WORKFLOW.md`: turn a paper into a draft explainer (notes, storyboard,
  video, one portrait short under three minutes, thumbnail, page, YouTube package), autonomously, up to human review. Use it to publish,
  process or resume a paper.
- `workflows/short-paper/WORKFLOW.md`: generate and independently review one short from a completed
  explainer. Also use for published-paper backfills, oldest research date first. Every new paper
  session must finish this companion before handover; approval checks it. Shorts remain local drafts.

In these workflows, the agent running the workflow and its subagents do the writing and visual reviews.
`paper-video` calls `agy` only for metadata when a PDF carries none. Never call
`claude -p` or an LLM API from the pipeline.

## Commands

- `uv run --frozen paper-video --help`: all pipeline commands.
- `uv run --frozen paper-video short <slug>`: build the portrait companion from `short.yaml`;
  `paper-video check <slug> short` checks the current output and independent review.
- `uv run --frozen aisr-site build`: build the site into `site/dist/`.
- `uv run --frozen aisr-site serve --drafts --media-root automations/media`: preview, including drafts.

## Publication and deployment

See [docs/deployment.md](docs/deployment.md) for Cloudflare setup and the publication sequence.
After the final video assembly, run `paper-video site <slug>` to refresh the hashed media mirror
before approval. With explicit user authorization, run `paper-video approve <slug>`, then
`cd site && npm run deploy`; verify both the public page and its referenced video. The deployment
guide records the R2 bucket/domain setup and the first publication's review results.

## Media backups

`automations/config.toml` is the canonical backup configuration. The approved Expansion drive root is
`/Volumes/Expansion/ROOT/Projects/Toronto (2026+)/AI Safety Risks/Media Backups/`.
`paper-video assemble <slug>` and `paper-video short <slug>` automatically back up their completed
exports there; this is already authorized and needs no confirmation on each run.

Snapshots live at `<backup-root>/<slug>/<content-key>/`, preserving `works/<slug>/out/`, narration,
and available source/edit metadata. Each has a SHA-256 manifest. Unchanged reruns verify and reuse
the snapshot; changed files create a new one. Require the configured volume to be mounted. A failed
backup fails the command while retaining the local video; report the failure and retry after the
drive is available. Binaries stay outside Git. See [docs/media-backup-plan.md](docs/media-backup-plan.md)
for the initial backup and archive details.

## Rules

- Scientific integrity comes before style: follow `automations/src/paper_video/prompts/integrity.md`.
- Never run `paper-video approve` or deploy unless the user asks. Approval marks a human review and
  uploads media to production.
