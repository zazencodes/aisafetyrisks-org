# aisafetyrisks.org

An educational site that explains AI safety research through animated explainers (Manim
Community), with every claim traced to a quote in the source paper. It is a `uv` workspace with
two packages:

- `site/`: static site generator (`aisr-site`) deployed to Cloudflare Workers static assets.
  Content lives in `site/content/`; output goes to `site/dist/`.
- `automations/`: `paper-video`, the deterministic steps of turning a paper into an explainer
  (ingest, provenance checks, narration, local Manim rendering, assembly, page and YouTube
  packaging). Configuration is in `automations/config.toml`, and every key is required. Per-paper
  work directories are in `automations/works/<slug>/`.

## Workflows

Workflows are step-by-step procedures for agents, in `workflows/<name>/WORKFLOW.md`. When a task
matches one, read the whole file before starting and follow it.

- `workflows/publish-paper/WORKFLOW.md`: turn a paper into a draft explainer (notes, storyboard,
  video, thumbnail, page, YouTube package), up to human review. Use it to publish, process or
  resume a paper.

In these workflows, the agent running the workflow and its subagents do the writing and visual reviews.
`paper-video` calls `agy` only for metadata when a PDF carries none. Never call
`claude -p` or an LLM API from the pipeline.

## Commands

- `uv run --frozen paper-video --help`: all pipeline commands.
- `uv run --frozen aisr-site build`: build the site into `site/dist/`.
- `uv run --frozen aisr-site serve --drafts --media-root automations/media`: preview, including drafts.
- `uv run pytest`: tests.

## Rules

- Scientific integrity comes before style: follow `automations/src/paper_video/prompts/integrity.md`.
- Never run `paper-video approve` or deploy unless the user asks. Approval records a named human
  reviewer and uploads media to production.
