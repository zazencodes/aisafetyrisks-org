# The Basic AI Drives — publication handover

Published: https://aisafetyrisks.org/works/the-basic-ai-drives/

- Original publication timestamp: `2026-10-03T11:31:16.528000-04:00`.
- Cloudflare deployment: `da50fec8-4db8-495b-8876-5fd395499289`.
- Exact public video: https://media.aisafetyrisks.org/works/the-basic-ai-drives/video-d5ab5b2a80ab.mp4
- Full video: 501.60 seconds (8:21.60), 1920×1080, 60 fps.
- Companion short: 126.60 seconds (2:06.60), 1080×1920, 30 fps; local draft.

## Outputs

Relative to this directory:

- Full video: `out/video.mp4`.
- Thumbnail: `out/thumbnail.jpg`.
- Full captions: `out/captions.vtt`, `out/captions.srt`.
- YouTube package: `youtube.yaml`; draft copy: `youtube-copy.yaml`.
- Page source: `site.yaml`; published content: `../../../site/content/works/the-basic-ai-drives/work.yaml`.
- Short: `out/short/video.mp4`.
- Short cover: `out/short/cover.jpg`.
- Short captions: `out/short/captions.vtt`, `out/short/captions.srt`.
- Short social package: `short-package.yaml`; edit: `short.yaml`; independent review: `short-review.yaml`.

Local preview: `uv run --frozen aisr-site serve --drafts --media-root automations/media`.

## Validation

All 35 notes claims have source-matched quotes. Storyboard and page science review 1 are accurate with no issues. All five scenes have current keyed visual reviews, with zero layout or visual issues. The full caption shape check passes: risk and method are clear by 67.5 seconds; the roadmap appears after the 84.6-second opening; each chapter answers its item; the closing returns to the chess machine and states the evidence boundary. No full-video shape failure remains.

The current short passes independent science and visual checks with no blocker or major issues. It retains the hypothetical setup, attribution, the condition “Unless designed otherwise,” resource externalities, a spoken limitation and takeaway. Whole narration beats are reused without speeding them up. The independent reviewer checked selected WAV lengths against segment lengths and found no duration truncation; listening verification remains limited as noted below.

All 3 site tests and 45 automation tests pass, along with the site build. Approval uploaded the reviewed long video and marked the page/backlog published. No YouTube, Instagram or Zernio posting was performed.

Live page, current video, thumbnail and captions return HTTP 200. The video is `video/mp4`, 27,488,401 bytes, with byte-range support; a tested request returns HTTP 206 and exactly 1,024 bytes. Downloaded thumbnail/captions match local outputs. Public browser playback succeeds without media errors; chapter clicks seek correctly and a fresh `#t=314` URL starts at 314 seconds.

Live canonical, VideoObject title/description/current media/duration/time-zone-aware uploadDate, Article/publisher metadata, chapter Clip links, sitemap video entry, robots sitemap pointer and HTTP-to-HTTPS redirect all pass. Search Console opened the signed-out introduction, so its Pages/Videos discovery reports remain unverified. The user subsequently removed Google's Rich Results Test from the workflow; it is not an outstanding check. No indexing claim is made.

## Open issues

All three are minor and confined to the short review:

1. **s04b04:** At the cut around 52.7 seconds, a diagram inherited from the omitted proxy/time-limit beat is visible briefly; it clears by 54 seconds. Narration and final resource diagram are coherent.
2. **s04b04:** Resource labels are small at 360-pixel phone width. Portrait headings and captions remain readable and convey the argument.
3. **s05b04 / review limitation:** Audible delivery and exact speech-to-caption alignment were not independently assessed because audio playback was unavailable to the reviewer. MP4 frames, captions, timing and complete source WAV durations were inspected.

No open storyboard/page science issue, full-scene visual issue, blocker, major issue or full-video shape failure remains.

## Backups

Full and short exports were archived and verified on Expansion. Final reviewed short/package snapshot:

`/Volumes/Expansion/ROOT/Projects/Toronto (2026+)/AI Safety Risks/Media Backups/the-basic-ai-drives/5ba0867d9fda5b464f10edac14176739925e7fc796b9c39202d3382801ca6267/`

The earlier deferred full/short backups for in-context scheming and anti-scheming training were retried successfully. The pending backup queue is empty. Local media and narration are retained.
