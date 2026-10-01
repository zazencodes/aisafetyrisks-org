# aisafetyrisks.org

Animated, source-grounded explanations of AI safety research. Each claim links to evidence
from the original paper.

The working video-generation pipeline is open source. The most useful contribution is to run
it on a research paper and submit a draft explainer. Budget roughly one five-hour Claude
session per video; this is a planning estimate, and usage varies with the paper, model and
revision work. ElevenLabs narration uses account credits, and local rendering takes compute time.

## Get started

See [CONTRIBUTING.md](CONTRIBUTING.md) for installation, choosing a paper, running the agent
workflow and submitting a draft. You can generate drafts without access to production accounts.

This is a `uv` workspace with two packages:

- `automations/`: the `paper-video` pipeline, paper backlog, Manim kit and per-paper work directories.
- `site/`: the `aisr-site` static site generator and Cloudflare Workers deployment.

The complete authoring procedure is [the publish-paper workflow](workflows/publish-paper/WORKFLOW.md).
Each paper includes one portrait short under three minutes, edited after the full video is
complete. The [short-form workflow](workflows/short-paper/WORKFLOW.md) also covers backfilling
published papers in research-date order; outputs are local drafts with captions and social copy.
Agent instructions are in [AGENTS.md](AGENTS.md).

## Maintainer publication

The [deployment guide](docs/deployment.md) covers Cloudflare setup, human approval, deployment
and public verification. Contributors submit drafts; Alexander reviews and publishes them.

## License

Copyright (C) 2026 Alexander Galea. Original project code, including the video-generation
pipeline and animation kit, is licensed under [GNU GPL version 3 only](LICENSE)
(`GPL-3.0-only`). Contributions to this code use the same license.

Bundled fonts and upstream material retain their own licenses; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The code license does not grant rights to
source papers, quoted passages, downloaded model weights or other third-party material.
