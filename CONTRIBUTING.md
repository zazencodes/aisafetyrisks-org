# Contributing a research explainer

The biggest help is to use your own agent session and computer to turn one paper into a draft.
Budget roughly one five-hour Claude session per video. This estimates agent usage, not guaranteed
elapsed time or a fixed subscription allowance; papers and revisions differ. Narration uses
ElevenLabs v4; Manim rendering runs locally.

## Install

Use Python 3.12 or 3.13, Git, [uv](https://docs.astral.sh/uv/getting-started/installation/),
FFmpeg, Cairo, Pango and pkg-config.
On macOS with Homebrew:

```sh
brew install uv ffmpeg cairo pango pkg-config
```

On Ubuntu/Debian, install the native dependencies before syncing Python packages:

```sh
sudo apt-get update
sudo apt-get install ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-dev build-essential
```

Install uv from the link above, and let uv install Python 3.12 if your system Python is outside
the supported range. LaTeX and dvisvgm are needed if scene code uses Manim's `Tex` or `MathTex`;
the bundled text components use Pango and the included fonts.

Fork [zazencodes/aisafetyrisks-org](https://github.com/zazencodes/aisafetyrisks-org) on GitHub,
then clone your fork and create a branch:

```sh
git clone https://github.com/YOUR-USERNAME/aisafetyrisks-org.git
cd aisafetyrisks-org
git switch -c paper/YOUR-PAPER-SLUG
uv sync --frozen --python 3.12
uv run --frozen paper-video --help
uv run --frozen aisr-site build
```

Use an agent environment that can read and write local files, run shell commands, launch fresh
subagents and inspect generated images. The workflow is agent-driven: `paper-video` performs
the deterministic steps, while the agent writes and reviews the material. It is not a single
command that calls Claude for you. Run the agent interactively with your own account.

Configuration is in `automations/config.toml`; every key is required. Draft generation needs
no Cloudflare or YouTube credentials. Narration requires an ElevenLabs API key with Text to
Speech access. Store it as `ELEVENLABS_API_KEY=...` in the repository root’s `.env` (ignored by
Git), and restrict the file with `chmod 600 .env`. Never commit the key. Voice, model, stability,
similarity and seed are explicit in `[tts]`. The configured model is `eleven_v4`, using Jarnathan.
Ingestion and narration require internet access. ElevenLabs generations consume account credits;
unchanged clips are cached, and each generated clip is saved immediately for resumable runs.
For key setup, voice selection, regeneration and review after a voice change, see
[ElevenLabs narration](docs/narration.md).
For arXiv papers, metadata comes from arXiv. A PDF without metadata needs the separately
installed and authenticated Antigravity CLI (`agy`) configured in `[agy]`; start with an arXiv
paper if you do not have that CLI.

## Choose one paper

Open a GitHub issue naming the queued paper you want to work on, and check existing issues to
avoid duplicating work. The backlog is `automations/backlog/papers.yaml`, oldest first.
Then give your agent this prompt from the repository root:

> Read AGENTS.md and automations/backlog/papers.yaml. Take the first queued paper that is not
> already claimed in a GitHub issue and follow workflows/publish-paper/WORKFLOW.md for it.
> Produce a draft for human review, and do not approve or deploy.

If you have claimed a specific paper, name it in the prompt instead. Follow the complete
workflow, including quotation checks, independent science reviews and scene visual reviews.
The scientific integrity rules are in `automations/src/paper_video/prompts/integrity.md`.

Preview your draft with:

```sh
uv run --frozen aisr-site serve --drafts --media-root automations/media
```

## Submit the draft

Open a pull request linked to your paper issue. Include:

- The paper's work directory: metadata, notes, storyboard, scene code, visual reviews, checks,
  page draft and YouTube package.
- The generated site page under `site/content/works/<slug>/` and the pipeline's backlog update.
- A summary of the paper, the report's open issues and a link to the draft video for review.

PDFs, audio, rendered video, frames and local media mirrors are ignored by Git. Share the
video separately using a downloadable link in the pull request; do not commit those binaries.
The generated site thumbnail and captions are included. A maintainer can re-fetch the pinned
paper and regenerate the media from your submitted source artifacts.

Check `git status` and review your diff before committing. Keep the change focused on your
paper. If you hit a pipeline bug, report it in an issue or submit a separate code change.

Stop at the workflow's handover. Alexander reviews the draft and runs approval and publication
with the production account. You do not need production access to contribute.

Original code contributions are accepted under GPL-3.0-only. Preserve third-party license
notices and cite source-paper quotations through the pipeline's provenance records.
Questions: [alex@galea.dev](mailto:alex@galea.dev).
