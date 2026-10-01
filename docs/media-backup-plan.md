# Expansion drive media backup

## Automatic backups

Creating a full video with `paper-video assemble <slug>` or a short with `paper-video short <slug>`
automatically archives that paper's completed exports, narration, and available source/edit metadata.
Alex has authorized these recurring backups; no additional confirmation is required.

The canonical configuration is the required `[backup]` section in `automations/config.toml`:

```toml
[backup]
volume = "/Volumes/Expansion"
root = "/Volumes/Expansion/ROOT/Projects/Toronto (2026+)/AI Safety Risks/Media Backups"
```

Each snapshot lives at `<root>/<slug>/<content-key>/` with a `manifest.json` recording file paths,
sizes, SHA-256 hashes, video kind, creation time, and source repository commit. The key covers the
archived files' content. Changed files create a new snapshot; unchanged reruns verify and reuse it.
Copies preserve `works/<slug>/` with `out/`, `audio/`, root YAML files, scene code, and available
short checks/report. No local source files are removed.

The configured volume must be mounted. Missing drives, insufficient space, changed source files
during copying, or failed verification fail the creation command while retaining its local video.
Reconnect the drive and rerun the same command after resolving the failure. An interrupted copy
remains marked `.in-progress`; inspect that incomplete snapshot before retrying. A snapshot is
promoted to its final name only after all copied file sizes and hashes pass verification. macOS
AppleDouble sidecars (`._*`) are outside the source-file manifest.

## Initial backup

Completed and hash-verified on 2026-10-01 after Alex approved the location.

Renamed `ROOT/Projects/Japan and Toronto (2025 - 2026)` to
`ROOT/Projects/Japan and Toronto (2025)`, preserving its contents. Created the new project archive
`ROOT/Projects/Toronto (2026+)` and placed this project inside it.

Backup location:
`/Volumes/Expansion/ROOT/Projects/Toronto (2026+)/AI Safety Risks/Media Backups/2026-10-01/`.

Each paper retains its existing directory layout under `works/<slug>/`:

- `out/`: full explainer, current short, captions, thumbnails, covers, timelines, and earlier exports.
- `audio/`: cached ElevenLabs narration and its manifest.
- Root YAML files and `scenes/*.py`: the paper metadata, verified notes, storyboard, scene code,
  short edit, review, social package, and YouTube copy used for these exports.
- `checks/short.json` and `checks/report.md`: current short validation and review results.

Includes all four papers:

- `concrete-problems-in-ai-safety`
- `the-off-switch-game`
- `goal-misgeneralization-in-deep-reinforcement-learning`
- `alignment-faking-in-large-language-models`

This includes 10 videos: four full explainers, four current shorts, and the Concrete Problems
`before-elevenlabs` and `before-jarnathan` versions. The current output folders and narration
and their accompanying files total 324 source files and 348,830,226 bytes (approximately 0.33 GiB).

`manifest.json` records every source file's relative path, byte count and SHA-256 hash, the source
repository commit (`606c901`), and the verification timestamp. Every copied file's size and hash
was checked against its source. The original local files remain in place. macOS AppleDouble
metadata sidecars (`._*`) are recorded separately from the 324 source files.

The repository already ignores every paper's `out/`, `audio/`, `render/`, and `frames/` folders.
Video and audio binaries remain outside Git; the backup snapshot preserves them separately.
