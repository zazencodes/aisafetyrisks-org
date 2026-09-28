# aisafetyrisks.org

Animated, source-grounded explanations of AI safety research. Each claim links to evidence
from the original paper.

This is a `uv` workspace with two packages:

- `automations/`: the `paper-video` pipeline, paper backlog, and per-paper work directories.
- `site/`: the `aisr-site` static site generator and Cloudflare Workers deployment.

## Working on a paper

Follow [the publish-paper workflow](workflows/publish-paper/WORKFLOW.md) to prepare a draft.
The backlog is in `automations/backlog/papers.yaml`; paper artifacts live in
`automations/works/<slug>/`.

From the repository root:

```sh
uv run --frozen paper-video --help
uv run --frozen aisr-site serve --drafts --media-root automations/media
```

## Deployment

Follow [the deployment guide](docs/deployment.md) for Cloudflare setup, finishing a reviewed
paper, approval, deployment, and public verification. Approval and deployment require an
explicit user request.

Agent instructions are in [AGENTS.md](AGENTS.md).
