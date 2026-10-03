# Published explainer — 2026-10-02

The user explicitly authorized finishing and publishing without personal review.

Public page: https://aisafetyrisks.org/works/stress-testing-deliberative-alignment-for-anti-scheming-training/
Video: https://media.aisafetyrisks.org/works/stress-testing-deliberative-alignment-for-anti-scheming-training/video-076ef71b2d69.mp4
Deployment version: `3fb5e5d3-bbd2-4936-ae08-9852f708ef23`.
Original publication timestamp: `2026-10-02T21:17:01.563680-04:00`.

## Completed artifacts

- Full video: [out/video.mp4](out/video.mp4), 546.5 seconds (9:06.5), 1920x1080.
- Thumbnail: [out/thumbnail.jpg](out/thumbnail.jpg).
- Full captions: [VTT](out/captions.vtt), [SRT](out/captions.srt).
- Page source: [site.yaml](site.yaml); YouTube package: [youtube.yaml](youtube.yaml).
- Portrait companion: [out/short/video.mp4](out/short/video.mp4), 138.20 seconds (2:18.2), 1080x1920.
- Short cover: [out/short/cover.jpg](out/short/cover.jpg).
- Short captions: [VTT](out/short/captions.vtt), [SRT](out/short/captions.srt).
- Short social copy/citation/links: [short-package.yaml](short-package.yaml).

No YouTube or social upload was performed; the companion remains a local draft.

## Validation

- All 45 note claims have source-verified quotes.
- Storyboard science review 2: accurate, no issues.
- Page science review 1: accurate, no issues.
- All six current scene renders: zero layout or visual issues, with keyed visual reviews.
- Full captions read from beginning to end: opening establishes risk and method within 81.287 seconds; each roadmap item is answered; closing returns to the opening's report and states the evidence boundary. No shape failure or timeline problems.
- Independent short science review: accurate, no issues. Short checks pass; package refreshed with review.
- All 3 site tests and 33 automation tests pass; site build succeeds.
- Public page/media/thumbnail/captions return HTTP 200. Video content type is video/mp4, content length 29,823,960 bytes; range request returns HTTP 206 with 1,024 bytes.
- Live canonical, VideoObject media/publication metadata, chapter URLs, video sitemap entry, robots sitemap pointer, and HTTP-to-HTTPS redirect verified.
- Public browser playback succeeds at 1920x1080, duration 546.5 seconds, with no media error. Published page visually inspected.
- Google Rich Results Test was attempted but returned “Log in and try again.” Search Console opened the signed-out introduction. No accessible authenticated Chrome/CDP session was found. Google eligibility/discovery reports remain unverified; indexing is not claimed.

## Minor notes

- Short s03b03: secondary chart labels are small at phone size; large heading, exclusion labels and spoken captions preserve the main point.
- Short audio: reviewer checked all selected WAV durations, complete clips and padding, but could not listen. Audible transition/caption timing was not verified by listening. Listen before any separate short-platform upload.
- Audience review had minor pacing notes about concentrated caveats in awareness and closing sections.
- Full runtime exceeds the brief's 5–8 minute target, with no failed runtime gate.

## Deferred backups

Backups are deferred maintenance, not blockers. Full and short exports are queued in
[automations/backlog/media-backups.md](../../backlog/media-backups.md), along with the earlier
in-context-scheming exports. Keep current local exports and narration until archived.

When Expansion is available, run from the repository root:

```sh
uv run --frozen paper-video backup-pending
```

This retries current files without rebuilding exports and removes only verified rows.
The pipeline, AGENTS.md, both publishing workflows, and backup guide now document this behavior.
