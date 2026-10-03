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

The main way to run this project is to work through the research shortlist,
`automations/backlog/papers.yaml`, one paper per agent session, oldest first. Only papers in that file
are processed; `automations/backlog/longlist.yaml` holds rejected candidates for reference.
Start a session with:

> Read `automations/backlog/papers.yaml` and follow the instructions at the top: take the first
> `queued` paper and run `workflows/publish-paper/WORKFLOW.md` for it.

Each paper's `status` in that file tracks its progress. The user has given standing authorization
to publish completed explainers to aisafetyrisks.org. For every requested paper session, including
"run the next paper", finish all required checks, run `paper-video approve <slug>` and deploy
autonomously as soon as ready. Do not wait for personal review or ask for publication confirmation.
An explicit draft-only or pause instruction takes precedence for that task.

## Workflows

Workflows are step-by-step procedures for agents, in `workflows/<name>/WORKFLOW.md`. When a task
matches one, read the whole file before starting and follow it.

- `workflows/publish-paper/WORKFLOW.md`: create and publish an explainer (notes, storyboard,
  video, one portrait short under three minutes, thumbnail, page, YouTube package) autonomously.
  Use it to publish, process or resume a paper.
- `workflows/short-paper/WORKFLOW.md`: generate and independently review one short from a completed
  explainer. Also use for published-paper backfills, oldest research date first. Every new paper
  session must finish this companion before handover; approval checks it. Shorts remain local drafts.
- `workflows/schedule-posts/WORKFLOW.md`: schedule the weekly release on Zernio, one published
  paper per week: the long-form video on YouTube on Tuesday, its short on YouTube Shorts and Instagram
  Reels on Thursday. Use it only when the user asks to schedule posts.

In these workflows, the agent running the workflow and its subagents do the writing and visual reviews.
`paper-video` calls `agy` only for metadata when a PDF carries none. Never call
`claude -p` or an LLM API from the pipeline.

## Commands

- `uv run --frozen paper-video --help`: all pipeline commands.
- `uv run --frozen paper-video short <slug>`: build the portrait companion from `short.yaml`;
  `paper-video check <slug> short` checks the current output and independent review.
- `uv run --frozen paper-video schedule`: upload and schedule the next paper's week through Zernio
  (`ZERNIO_API_KEY` in `.env`); `paper-video schedule-status` reads each post's status back.
- `uv run --frozen aisr-site build`: build the site into `site/dist/`.
- `uv run --frozen aisr-site serve --drafts --media-root automations/media`: preview, including drafts.

## Publication and deployment

See [docs/deployment.md](docs/deployment.md) for Cloudflare setup and the publication sequence.
After the final video assembly, run `paper-video site <slug>` to refresh the hashed media mirror
before approval. Under the standing publication authorization, run `paper-video approve <slug>`, then
`cd site && npm run deploy`; verify both the public page and its referenced video. The deployment
guide records the R2 bucket/domain setup and the first publication's review results.

## Media backups

`automations/config.toml` is the canonical backup configuration. The approved Expansion drive root is
`/Volumes/Expansion/ROOT/Projects/Toronto (2026+)/AI Safety Risks/Media Backups/`.
`paper-video assemble <slug>` and `paper-video short <slug>` automatically back up their completed
exports there; this is already authorized and needs no confirmation on each run.

Snapshots live at `<backup-root>/<slug>/<content-key>/`, preserving `works/<slug>/out/`, narration,
and available source/edit metadata. Each has a SHA-256 manifest. Unchanged reruns verify and reuse
the snapshot; changed files create a new one. Backups are deferred work, never a blocker for
generation or authorized publication. If the drive is unavailable or a backup fails, the command
retains local files, reports the reason and upserts a paper/export row in
`automations/backlog/media-backups.md`. Continue the workflow and say the backup will be updated
later; do not ask the user to connect the drive or pause. Keep unarchived exports and narration.
When the drive is available, run `uv run --frozen paper-video backup-pending`; it archives current
files without rerendering and removes only verified entries. Binaries stay outside Git. See
[docs/media-backup-plan.md](docs/media-backup-plan.md) for backlog and archive details.

## SEO maintenance

- Every published explainer requires `site/content/works/<slug>/impact.yaml` for its
  “Why this paper matters today” section. Follow [docs/paper-impact.md](docs/paper-impact.md):
  this separately sourced editorial context covers later research, with verified primary-source
  passages and optional dated citation counts. It survives `paper-video site` regeneration.
- Every explainer page must render `VideoObject` JSON-LD with its visible title/summary,
  absolute thumbnail and current hashed media URL, actual duration, and time-zone-aware original
  publication timestamp (`published_at` → `uploadDate`). Keep Article, publisher, and chapter Clip
  metadata consistent with the page and working `#t=<seconds>` links. Never invent dates or statistics.
- `aisr-site build` automatically regenerates `/sitemap.xml` with all public pages and video
  entries for published explainers, plus `/robots.txt` pointing to that sitemap. Extend the
  generator when adding page types; do not maintain a separate hand-written URL list.
- Drafts must remain `noindex` and excluded from the sitemap/feed; the 404 page is `noindex`.
  Preserve unique titles/descriptions, absolute canonical URLs, crawlable thumbnails/captions,
  and publicly accessible video files with byte-range support.
- `paper-video approve` records `published_at` on first publication and `updated_at` on updates;
  page regeneration preserves publication metadata. Preserve `published_on` and `published_at`
  when updating an explainer. Record actual `updated_on`/`updated_at` for substantive changes
  so sitemap `lastmod` remains truthful. Do not stamp unchanged pages on every build.
- Before a site deployment, run `uv run --frozen python -m unittest discover -s site/tests`,
  `uv run --frozen python -m unittest discover -s automations/tests`,
  and `uv run --frozen aisr-site build`. After deployment, verify the live sitemap, robots,
  video markup and referenced media. Use Search Console's Pages/Videos reports to check discovery;
  valid markup does not promise indexing. Google's Rich Results Test is outside the publication
  workflow: do not run it or record it as an expected or deferred check.
- Search Console uses the `aisafetyrisks.org` Domain property and the single sitemap URL
  `https://aisafetyrisks.org/sitemap.xml`. Preserve its Google verification TXT record in DNS.
- Keep Cloudflare's Always Use HTTPS enabled; verify HTTP URLs redirect to their HTTPS
  equivalents. See `docs/deployment.md` for the Search Console setup and remaining checks.

## Integrity and publication rules

- Scientific integrity comes before style: follow `automations/src/paper_video/prompts/integrity.md`.
- Standing authorization covers approval, production media upload and site deployment for completed
  paper sessions. Publish after source checks, independent science/visual reviews, companion-short
  checks and deployment checks pass; personal review is not required. Do not bypass failed checks
  or unresolved blocker/major review issues. Report minor issues and deferred backups after publishing.
- YouTube and Instagram posting needs the user's explicit request in that task; standing publication
  authorization does not cover it. Follow `workflows/schedule-posts/WORKFLOW.md`.
