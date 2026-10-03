# Publication handover

Published: https://aisafetyrisks.org/works/behavior-purpose-and-teleology/
Deployment: `e7dcac12-5d15-4d2c-9e64-82741dba8f8a`.

Source: archive.org retypeset PDF; canonical attribution https://doi.org/10.1086/286788.
Research date is January 1943. The backlog's January first is a sorting placeholder, not an asserted day. Visible research dates and ScholarlyArticle metadata now use month precision throughout the site.

32 source-verified claims. Audience review had no major issues; four minor phrasing issues were addressed. Storyboard science review 1 and page science review 1: accurate, no issues. All five scenes have current visual reviews with no layout or visual issues. Captions read in full: opening establishes the hypothetical risk and paper within 63 seconds; roadmap and chapters correspond; closing returns to the robot and states the evidence boundary. No shape failures.

Full video: `out/video.mp4`, 394.60 seconds, 1920×1080. Thumbnail: `out/thumbnail.jpg`; captions: `out/captions.vtt`; YouTube package: `youtube.yaml`. Site content: `site/content/works/behavior-purpose-and-teleology/`. Preview: `uv run --frozen aisr-site serve --drafts --media-root automations/media`.

Portrait draft: `out/short/video.mp4`, 137.00 seconds, 1080×1920, 30 fps. Cover: `out/short/cover.jpg`; captions: `out/short/captions.srt` and `out/short/captions.vtt`; social package: `short-package.yaml`. Current independent review passes, science accurate. Open minor notes:
- s02b03 briefly inherits active/passive labels at the cut before the goal diagram replaces them.
- Listening-based pronunciation and caption-to-speech synchrony were unavailable to the reviewer; WAV duration and caption endpoint checks passed.
The review file and passing check were written before the reviewer later reported a usage-limit error. No further review is claimed.

All 3 site tests and 45 automation tests passed; production build passed. Live page, exact video URL, thumbnail and captions return 200. Video: `video/mp4`, 20,541,247 bytes; byte range returned 206 and 1,024 bytes. Public browser playback and chapter seeking work. Canonical/video/chapter metadata, original publication timestamp, sitemap entry, robots pointer and HTTP-to-HTTPS redirect verified. Citation snapshot: OpenAlex W2022305914, 1,577, verified original article record, retrieved 2026-10-03. Preview and live page show correct attribution and scope.

Full and short Expansion snapshots verified. No deferred backup work. No YouTube, Instagram or Zernio posting.

The pipeline's backlog matcher uses the DOI source URL rather than the PDF input and therefore did not match this backlog entry. The existing `backlog.set_status` function was invoked with the PDF URL after ingestion and successful approval; status was never edited manually. No pipeline changes were made.

Search Console opened Google's sign-in screen. Pages/Videos discovery reports remain unverified; no indexing claim is made.
