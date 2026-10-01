# Expansion drive media backup plan

Awaiting Alex's approval before creating folders or copying files onto the drive.

Proposed snapshot: `/Volumes/Expansion/aisafetyrisks.org/video-backups/2026-10-01/`.
The drive is mounted with approximately 4.5 TiB available. This folder does not yet exist.

Preserve each paper's existing directory layout under `works/<slug>/`:

- `out/`: full explainer, current short, captions, thumbnails, covers, timelines, and earlier exports.
- `audio/`: cached ElevenLabs narration and its manifest.
- Root YAML files and `scenes/*.py`: the paper metadata, verified notes, storyboard, scene code,
  short edit, review, social package, and YouTube copy used for these exports.
- `checks/short.json` and `checks/report.md`: current short validation and review results.

Include all four papers:

- `concrete-problems-in-ai-safety`
- `the-off-switch-game`
- `goal-misgeneralization-in-deep-reinforcement-learning`
- `alignment-faking-in-large-language-models`

This includes 10 videos: four full explainers, four current shorts, and the Concrete Problems
`before-elevenlabs` and `before-jarnathan` versions. The current output folders and narration
occupy approximately 0.33 GiB combined; the accompanying text files add little to that total.

After approval, create a new snapshot, copy the listed files without removing the originals,
and write a manifest containing each relative path, byte count, SHA-256 hash, and repository
commit. Compare every copied file's size and hash against its source, then report the verified
video count and destination. Stop if the destination already exists or the drive is unavailable.

The repository already ignores every paper's `out/`, `audio/`, `render/`, and `frames/` folders.
Video and audio binaries remain outside Git; the backup snapshot preserves them separately.
