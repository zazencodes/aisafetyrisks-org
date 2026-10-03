# Publication completed — 2026-10-02

Paper: Frontier Models are Capable of In-context Scheming.
The user authorized completion and deployment on 2026-10-02. The work and backlog are now published.
Media backup remains explicitly deferred because Expansion is unmounted.

## Completed

- Source notes: 39 claims, all evidence quotes found in the extracted paper.
- Storyboard: provenance passes; final independent science review accurate, zero issues.
- Narration and all five scene renders: current visual reviews, zero layout or visual issues.
- Local full video: `out/video.mp4`, 433.6 seconds (7:13.6).
- Full captions: `out/captions.vtt` and `out/captions.srt`.
- Thumbnail: `out/thumbnail.jpg`, checked visually.
- Draft page generated and independently science-reviewed: accurate, zero issues.
- YouTube package: `youtube.yaml`.
- Portrait short: `out/short/video.mp4`, 159.6 seconds (2:39.6); independent science/visual review passed.
- Short cover, SRT/VTT captions and reviewed draft `short-package.yaml` generated.
- Site build passed; draft preview and referenced video returned HTTP 200.

## Deferred media backup

The user explicitly authorized continuing on 2026-10-02 and backing up later.
Both full and short exports are retained locally. Their commands reached the backup step and
reported `/Volumes/Expansion` unmounted. This is pending work, not a blocker to draft completion.
The configured destination remains unchanged.

When Expansion is connected, run these existing commands to create and verify snapshots:

```sh
uv run --frozen paper-video assemble frontier-models-are-capable-of-in-context-scheming
uv run --frozen paper-video short frontier-models-are-capable-of-in-context-scheming
```

Do not delete the local exports or narration until backup verification succeeds.

## Review observations

Caption shape check: no failure. The hypothetical inbox risk and what the paper did are
established by 1:10; chapters answer the roadmap in order; closing returns to the inbox,
attributes recommendations, states the evidence boundary, and ends with a process-tracing takeaway.

Final science review and scene visual reviews have no open issues. Audience review's major
incentive-clarity issue was corrected. Minor audience pacing suggestions remain: consecutive
qualifications in s03b05–06, secondary examples in s04b01–02, late capability/propensity
framing in s04b06, and repeated boundaries in s05b03. The abstract diagram labels were made
explicit during scene implementation; the safety-argument wording was clarified.

## Final short review

Science verdict: accurate; no major or blocking science/visual issues. Current short check passes
at 159.60 seconds. Minor review notes: recommendation labels inherited briefly at the limitation
cut; some inset diagram labels are small at phone size; audio playback was not auditioned.
Narration durations fit the edit windows without truncation.

Draft preview: http://localhost:8010/works/frontier-models-are-capable-of-in-context-scheming/

The full explainer is published. The portrait companion and YouTube package remain local drafts.
Backup remains explicitly deferred; local exports and narration are retained.


## Publication verification

- Current render checks passed for all five scenes, with no layout or visual issues.
- Current independent short review/check passed at 159.60 seconds; minor notes above remain.
- Refreshed the page/media mirror after the existing final assembly; page provenance passed.
- Required site tests: 3 passed. Required automation tests: 31 passed. Site build passed.
- Approval uploaded `works/frontier-models-are-capable-of-in-context-scheming/video-38dd01c271e8.mp4`
  and recorded publication at `2026-10-02T20:33:50.030547-04:00`.
- Deployment version: `808eadf0-d8ca-46ae-b72c-d1d181c0573c`.
- Public page: https://aisafetyrisks.org/works/frontier-models-are-capable-of-in-context-scheming/
- Live page, exact video, thumbnail and captions returned HTTP 200. The video is `video/mp4`,
  23,153,629 bytes; a 1,024-byte range request returned HTTP 206 with the correct Content-Range.
- Live VideoObject references the current media URL and actual publication timestamp.
  Sitemap XML includes this page and video; robots.txt points to the sitemap. Page has no noindex.
  HTTP page URL redirects to its HTTPS equivalent with HTTP 301.
- Search Console processing/indexing and Google's Rich Results Test for this new page were not
  checked in this session; the HTTP and metadata checks do not establish indexing.
- No media backup was attempted in this session, and no YouTube/social upload was performed.
