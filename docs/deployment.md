# Deployment

## Architecture and configuration

The HTML site is an assets-only Cloudflare Worker named `aisafetyrisks-org`, served at
`https://aisafetyrisks.org`. `npm run deploy` in `site/` invokes Wrangler, whose build hook
runs `uv run --frozen aisr-site build` and uploads `site/dist/`.

Videos live separately in the R2 bucket `aisafetyrisks-media`, served through its custom
domain `https://media.aisafetyrisks.org`. Thumbnail images and captions are site assets.
Video object names include a content hash and use an immutable cache policy.

The configuration sources are:

- [`site/wrangler.jsonc`](../site/wrangler.jsonc): Worker, build hook, assets, and site domain.
- [`site/package.json`](../site/package.json): deployment command and Wrangler version.
- [`automations/config.toml`](../automations/config.toml): publication bucket and site URL.
- [`site/content/site.yaml`](../site/content/site.yaml): site and media base URLs.

## Cloudflare setup

Use Python 3.12 or 3.13, `uv`, Node.js, and npm. Install the pinned JavaScript dependencies
with `npm ci` in `site/`. The domain's Cloudflare zone and deployment credentials must belong
to the intended account. Verify authentication before provisioning or deploying:

```sh
cd site
npx wrangler whoami
npx wrangler r2 bucket list
```

The production resources were provisioned in the **ZazenCodes** account
(`44ff604d9938c2ba69da4220e33a1d0c`). The `aisafetyrisks.org` zone ID is
`b1550c3cf850b3e61c733f7b4b51c301`. These identifiers are not credentials. If setting up
another account, obtain its own zone ID from Cloudflare and use that account's credentials.

The following setup was completed on 2026-09-28. Run it only when provisioning missing
resources, after checking the account and existing bucket/domain configuration:

```sh
npx wrangler r2 bucket create aisafetyrisks-media
npx wrangler r2 bucket domain add aisafetyrisks-media \
  --domain media.aisafetyrisks.org \
  --zone-id b1550c3cf850b3e61c733f7b4b51c301 \
  --min-tls 1.2 --force
```

Confirm the connection with:

```sh
npx wrangler r2 bucket domain list aisafetyrisks-media
```

Wrangler authentication stays in its local credential store. Do not copy tokens into the
repository or documentation.

## Finish and publish a reviewed paper

Follow [the full workflow](../workflows/publish-paper/WORKFLOW.md) for authoring, scene
subagent prompts, science review prompts, and correction rules. The user has given standing
authorization for completed paper sessions to approve and deploy as soon as all required checks
pass. Do not wait for personal review or request publication confirmation. Explicit draft-only or
pause instructions take precedence. Independent reviews and automated checks still apply.
Deferred Expansion backups in
`automations/backlog/media-backups.md` do not block approval or deployment. Additional science
review rounds beyond its limits also need authorization.

Run all `paper-video` commands from the repository root, replacing `<slug>`:

1. Run `uv run --frozen paper-video render <slug>`. For every scene listed as needing work or
   a current visual review, start a scene subagent with the exact prompt from workflow step 5.
   Re-run render after the agents finish until it exits successfully. An already rendered
   scene can need only a visual review; the review must use its current render key.
2. Run `uv run --frozen paper-video assemble <slug>`. Address any timeline failures according
   to workflow step 6. Read `automations/works/<slug>/out/captions.vtt` in full to check the
   opening, roadmap, chapter coverage, and closing.
3. Run `uv run --frozen paper-video site <slug>` **after the final assembly**, even if the page
   was already built. This regenerates `site/content/works/<slug>/work.yaml`, copies captions
   and thumbnail, and refreshes the hashed video in `automations/media/works/<slug>/`.
   It writes the page with `status: draft`, so it must precede approval.
4. Run the required science reviews using fresh subagents with the workflow step 3.3 prompt
   for `review-storyboard` and `review-site`. Reviews are recorded against the content they
   examined. Fix blocker or major issues with the smallest supported edit and review again
   within the authorized round limit. A storyboard edit requires checking, narration,
   affected scene renders, assembly, and page regeneration before publication.
5. Under standing publication authorization, approve once all required checks pass:

   ```sh
   uv run --frozen paper-video approve <slug>
   ```

   Approval rechecks page provenance and current science reviews, rejects unresolved blocker
   or major issues, uploads the mirrored video to R2, marks the page published, records the
   approval date, and updates the backlog. Minor issues can remain and must be reported.
6. Deploy the site:

   ```sh
   cd site
   npm run deploy
   ```

   Wrangler rebuilds the site before uploading it. Record the successful deployment's
   version ID. This publishes all current site content and static assets in the workspace.

To deploy a site-only change after authorization, use step 6. If changing a published paper's
content or media, repeat the applicable generation/review steps and approval first.
For a voice change, use [the ElevenLabs narration guide](narration.md) to regenerate audio,
re-render scenes, assemble, and refresh the page before approval.

## Verification and failure recovery

Google's Rich Results Test is outside the publication workflow. Do not run it or record it as an
expected or deferred check. Validate the live video markup directly and use Search Console's
Pages/Videos reports for discovery monitoring.

Check both the published page and the exact video URL. Read `video.key` from
`site/content/works/<slug>/work.yaml` and append it to the configured media base URL:

```sh
curl -I https://aisafetyrisks.org/works/<slug>/
curl -I https://media.aisafetyrisks.org/<video.key>
```

Both should return HTTP 200; the video should have `Content-Type: video/mp4`, a nonzero
content length, and byte-range support. Also check that the live page references the current
video key. `uv run --frozen paper-video report <slug>` summarizes local checks and open issues.

- **“The specified bucket does not exist” during approval:** check `wrangler whoami` and the
  bucket list. Provision the configured bucket and media domain if missing, then repeat
  approval. An upload failure occurs before the page/backlog are marked published; wait for
  approval to succeed before deployment.
- **Missing or stale science review:** review the current content with the workflow subagent
  prompt. Editing reviewed prose or the storyboard invalidates its recorded review.
- **Wrong video after reassembly:** repeat `paper-video site <slug>` before approval. Approval
  uploads the page's referenced local mirror, not `out/video.mp4` directly.
- **Deployment failure after approval:** resolve the reported deployment error and rerun
  `npm run deploy`. A successful media upload alone does not deploy the HTML site.

During the first publication, Python `urllib` HEAD requests returned HTTP 403 while `curl -I`
returned HTTP 200 for both URLs. Recheck with curl before diagnosing a failed deployment
from a client-specific response.

## First publication record: 2026-09-28

`concrete-problems-in-ai-safety` was finished and published with explicit authorization for
approval, deployment, and a third science review round:

- Render initially requested a current visual review for s05. Its subagent inspected the
  contact sheet and updated `visual-reviews/s05.yaml` to render key `a5ed89e90470bc27`;
  no scene code change was needed. The final render passed with no layout or blocker/major
  visual issues. Existing minor visual issues remained in other scenes.
- Assembly produced `out/video.mp4` (reported as 467 seconds). The captions passed the shape
  review. The page was regenerated after assembly and passed provenance checks with 16 claims.
- Storyboard science review 3: accurate, no issues. Site science review 3: accurate, one minor
  clarity issue in `explanation[3].body` about “the best measure”; no blocker or major issues.
  Review details are in the work directory's `checks/reviews/` and `checks/reviews.json`.
- The first approval failed because the R2 bucket was missing. The bucket and media custom
  domain were created using the setup above. Approval then uploaded
  `works/concrete-problems-in-ai-safety/video-aac74655fe44.mp4` and marked the work published.
- Deployment succeeded with version ID `8dd70906-06ad-4782-84fa-10222db5872c`.
  The [public page](https://aisafetyrisks.org/works/concrete-problems-in-ai-safety/) and its
  video returned HTTP 200 using curl.

The paper's source artifacts are in `automations/works/concrete-problems-in-ai-safety/`:
`storyboard.yaml`, `site.yaml`, scene code, visual reviews, `out/video.mp4`,
`out/captions.vtt`, `out/thumbnail.jpg`, and `youtube.yaml`. The generated page is in
`site/content/works/concrete-problems-in-ai-safety/`. The YouTube package is a local artifact;
this publication did not upload a video to YouTube.

## Jarnathan narration update: 2026-09-28

The maintainer selected Jarnathan (`c6SfcYrb2t09NHXiT80T`) for the published explainer.
Following [the narration guide](narration.md), all 38 clips were regenerated with Eleven v4,
all eight scenes were rendered and visually reviewed, and the 493-second video was reassembled.
All 38 source clips matched the final soundtrack at their expected positions; the existing
storyboard and page science reviews remained current. The page was refreshed, approved, and
deployed with `works/concrete-problems-in-ai-safety/video-64c977069037.mp4`. The deployment
version was `f92e10d1-7a6d-49fb-b6fe-8dd4d8ee2864`. The live page and video returned HTTP
200, and the video supported byte ranges. Five minor visual readability issues remain in scenes
s01, s02, s06, and s07; there are no blocker or major visual issues.

## Goal misgeneralization publication: 2026-09-30

The maintainer authorized finishing and publishing
`goal-misgeneralization-in-deep-reinforcement-learning`. The storyboard was corrected to
remove unsupported detection claims, distinguish critic value from reward, and limit the
training-diversity conclusion to the observed CoinRun improvement. The spoken Maze result
now includes its trial exclusion. The YouTube description was corrected to match.

All 23 narration clips were regenerated with the configured Jarnathan voice. All six scenes
passed current visual reviews with zero layout or visual issues. Assembly produced a
257-second video; the captions passed the opening, roadmap, chapter, and closing check.
Storyboard science review 5 and site science review 4 were accurate with no blocker or major
issues. One minor storyboard issue remains: the 100% permeable-wall result omits `n = 114`
in the video display; the page includes it.

The page was refreshed after assembly, approved, and deployed with video key
`works/goal-misgeneralization-in-deep-reinforcement-learning/video-7886099f0396.mp4`.
Deployment version: `c0945218-3472-49bf-81f9-a6b88f8dd57d`. The public page and exact video
returned HTTP 200; the video was served as `video/mp4` with byte-range support and a
17,748,440-byte content length. Browser playback succeeded locally and publicly.
The YouTube package remains a local artifact; this publication did not upload to YouTube.

After a fresh draft review on 2026-09-30, storyboard science review 6 and site science review 5
again found no blocker or major issues; the same minor sample-size omission remains. The
maintainer approved publication, and the current video was uploaded and the site redeployed
with version `fa6ffcb3-cb7a-4adf-bbfb-afe689fd2171`. Curl verification returned HTTP 200
for the public page and its referenced `video-7886099f0396.mp4`; the video retained its
17,748,440-byte length, `video/mp4` content type, and byte-range support.

## Alignment faking publication: 2026-10-01

The maintainer reviewed and approved `alignment-faking-in-large-language-models` after the
opening animation was rebuilt. The replacement opening lasts 67.566667 seconds and preserves
every original beat boundary. The final decoded soundtrack hash matched the reviewed original;
audio sources, later scene code and renders, captions, and timeline remained unchanged.

All seven scenes have current visual reviews with no layout or visual issues. Storyboard science
review 1 and site science review 2 are accurate with no blocker or major issues. One minor
storyboard issue remains: the closing does not explicitly qualify the model's open admissions
as observed before reinforcement learning. The page's initial major issue about the prompted
setup's reliance on a hidden scratchpad was corrected before its final review.

Approval uploaded the 475-second, 1920×1080 video as
`works/alignment-faking-in-large-language-models/video-f7b1b6a084ea.mp4` and marked the
page and backlog published. The doomsday page now links to the explainer beside its paper citation.
Deployment version: `a53eeca1-99cd-4012-8cc4-2de4f22e7ea8`. The public page references
that exact video key. Both returned HTTP 200; the video has `video/mp4` content type and a
28,917,554-byte content length. A byte-range request returned HTTP 206 with the expected
1,024-byte response. The YouTube package remains a local artifact; this did not upload to YouTube.

## SEO and Search Console setup: 2026-10-01

The `aisafetyrisks.org` Domain property was added in Chrome under the maintainer's Google
account. The maintainer added the verification TXT record through Cloudflare; Google's
ownership check succeeded. Keep that DNS record in place. The submitted sitemap URL is
`https://aisafetyrisks.org/sitemap.xml`; Google periodically checks that URL for updates.
The homepage's URL Inspection indexing request also succeeded; the UI confirmed
**Indexing requested**. This queues a crawl and does not mean the page is already indexed.

The build includes Google's video sitemap extension for all four published explainers,
alongside the homepage and three editorial pages. Video titles, descriptions, thumbnails,
media URLs, and publication timestamps match the rendered `VideoObject` metadata. Drafts
stay outside the sitemap/feed, and drafts and the 404 page have `noindex` metadata.

Google's Rich Results Test successfully crawled the alignment-faking page and detected
a valid VideoObject without video warnings after the timestamp correction. The source-paper
ScholarlyArticle metadata has optional article warnings where exact publication times and
author profile URLs are unavailable; do not invent these to satisfy recommendations.
Article `dateModified` is emitted only when an actual `updated_at` has been recorded.

Original `published_at` timestamps were recovered from the **deployment** creation times
in `wrangler deployments list`, using the first production version that published each work:

- Concrete problems: `8dd70906-06ad-4782-84fa-10222db5872c`, `2026-09-28T15:01:25.185Z`.
- Off-switch game: `4322af6d-f977-4a2a-ab60-1cf44d6bc37b`, `2026-09-29T06:11:27.585Z`.
- Goal misgeneralization: `c0945218-3472-49bf-81f9-a6b88f8dd57d`, `2026-09-30T17:27:32.986Z`.
- Alignment faking: `a53eeca1-99cd-4012-8cc4-2de4f22e7ea8`, `2026-10-01T04:15:05.836Z`.

Future first approvals record a time-zone-aware `published_at`, and subsequent approvals
record `updated_at`. Regenerating a page retains the original dates/timestamps. These
metadata changes do not approve new papers or alter their reviewed scientific prose.

The final SEO deployment is `fdd153b2-9870-4245-814a-3bad1b112760`. Checks passed for all
eight public pages, all four videos and their thumbnails/captions, sitemap XML against the
official sitemap and video-extension XSDs, canonical URLs, robots.txt, and the HTTP 404
response. Three site tests and eight automation tests passed, including mocked publication
tests that never upload media. Cloudflare's Always Use HTTPS was enabled and verified:
HTTP URLs return 301 to their HTTPS equivalents, which return 200.

Search Console initially reported **Couldn't fetch** for the submitted sitemap, including
after one resubmission. Public fetching returns HTTP 200/application/xml, XML validation
passes, and Google's rich-results crawler reaches the site. Recheck the Sitemaps report
after Google's processing catches up; do not describe the sitemap as successfully processed
until the report confirms it. The new property's performance/indexing reports are also
still processing. Check Pages, Videos, and Core Web Vitals once data is available.

Keep publishing useful source-grounded explainers, link related research and topic pages,
and review search queries/impressions before changing titles. Publish the prepared YouTube
packages when authorized, link to their canonical explainers, and set the real YouTube URLs
in content. Validate future video pages' live structured data directly and follow Google's
[video SEO guidance](https://developers.google.com/search/docs/appearance/video).


## In-context scheming publication: 2026-10-02

The maintainer authorized finishing and deploying
`frontier-models-are-capable-of-in-context-scheming`, explicitly deferring media backup while
Expansion is unmounted. Existing final exports and current independent reviews passed; all five
scenes have zero layout or visual issues. The reviewed 159.60-second portrait companion remains a
local draft with its minor review notes recorded in the work's HANDOVER.md.

The page/media mirror was refreshed, approval uploaded the 433.6-second full video as
`works/frontier-models-are-capable-of-in-context-scheming/video-38dd01c271e8.mp4`, and the
backlog/page were marked published. Publication timestamp: `2026-10-02T20:33:50.030547-04:00`.
All 3 site tests and 31 automation tests passed, as did the site build.
Deployment version: `808eadf0-d8ca-46ae-b72c-d1d181c0573c`.

The public page, referenced video, thumbnail and captions returned HTTP 200. Video content type
is `video/mp4`, with a 23,153,629-byte length; a range request returned HTTP 206 and the expected
1,024 bytes. Live VideoObject media/publication metadata, sitemap entry, robots sitemap pointer,
and HTTP-to-HTTPS redirect passed verification. Search Console and Rich Results Test were not
checked for this page during this session. Backup remains pending; local media and narration are
retained. No YouTube/social upload was performed.

## Anti-scheming training publication: 2026-10-02

The maintainer authorized finishing and publishing
`stress-testing-deliberative-alignment-for-anti-scheming-training` without personal review.
The source notes, storyboard, page and all six scenes pass their provenance/science/visual
checks. The 138.20-second portrait companion passes its independent review and remains local.
Two minor short review notes concern small secondary chart labels and unavailable listening
verification; details are recorded in the work's HANDOVER.md.

Approval uploaded the 546.5-second full video as
`works/stress-testing-deliberative-alignment-for-anti-scheming-training/video-076ef71b2d69.mp4`.
Publication timestamp: `2026-10-02T21:17:01.563680-04:00`.
All 3 site tests and 33 automation tests passed, as did the site build.
Deployment version: `3fb5e5d3-bbd2-4936-ae08-9852f708ef23`.

The public page, exact video, thumbnail and captions return HTTP 200. The video is
`video/mp4`, 29,823,960 bytes, with byte-range support; the tested range returned HTTP 206
and 1,024 bytes. Public browser playback succeeds with no media error. Live canonical,
VideoObject/chapters, sitemap, robots and HTTP-to-HTTPS redirect checks pass. Google's
Rich Results Test requested login, and Search Console opened its signed-out introduction;
Google eligibility/discovery reports remain unverified. No indexing claim is made.

The maintainer also requested permanent backup deferral. Assembly and short generation now
report archive failures and upsert the tracked `automations/backlog/media-backups.md` queue,
then continue. `paper-video backup-pending` retries current local files and removes only
verified entries. Expansion backups for this work and the earlier in-context-scheming work
remain queued; local exports and narration are retained. AGENTS.md, both paper workflows and
the backup guide document this policy. No YouTube/social upload was performed.

## Basic AI Drives publication: 2026-10-03

Processed the first queued paper, Omohundro’s *The Basic AI Drives*, under standing publication
authorization. The 35 source-verified claims distinguish conceptual arguments, hypothetical examples,
exceptions and author proposals. Storyboard/page science review 1 passed with no issues. All five
scenes passed current visual reviews with zero layout or visual issues. The 501.60-second full video
passes the caption shape check. Its 126.60-second portrait companion passes independent review and
remains a local draft; three minor short notes are recorded in the work’s HANDOVER.md.

Approval uploaded `works/the-basic-ai-drives/video-d5ab5b2a80ab.mp4` and recorded original
`published_at: 2026-10-03T11:31:16.528000-04:00`. Deployment version:
`da50fec8-4db8-495b-8876-5fd395499289`. All 3 site tests and 45 automation tests passed, as did the
site build. Public page/video/thumbnail/captions, byte ranges, canonical/video/chapter metadata,
sitemap, robots and HTTP-to-HTTPS redirect pass verification. Public browser playback and chapter
seeking work. The video is `video/mp4`, 27,488,401 bytes; the tested range returned 206/1,024 bytes.

Google’s Rich Results Test returned “Log in and try again,” and Search Console showed its signed-out
introduction. The user subsequently removed the Rich Results Test from the workflow; it is not an
outstanding check. Search Console discovery reports remain deferred; no indexing claim is made.
Expansion backups for this paper verified successfully. `paper-video backup-pending` also completed
the earlier in-context-scheming and anti-scheming-training full/short backups; the queue is now empty.
No YouTube, Instagram or Zernio posting was performed.

## Behavior, Purpose and Teleology publication: 2026-10-03

Published https://aisafetyrisks.org/works/behavior-purpose-and-teleology/ under standing authorization.
The archive.org retypeset PDF is attributed to DOI `10.1086/286788`; research date is January 1943.
Research dates now display month/year and use month precision in ScholarlyArticle metadata, avoiding
an invented day for issue-dated works. Explainer publication timestamps remain precise.

32 verified claims, accurate storyboard/page science reviews with no issues, and five current scene
reviews with zero layout/visual problems. Full video: 394.60 seconds. Local portrait draft: 137.00 seconds,
passing independent review with two minor notes (brief inherited labels at a cut and unavailable
listening verification), detailed in the work's HANDOVER.md. Both Expansion backups verified.
All 3 site tests and 45 automation tests passed; build passed.

Deployment: `e7dcac12-5d15-4d2c-9e64-82741dba8f8a`. Exact video:
`works/behavior-purpose-and-teleology/video-97023db4873d.mp4`, 20,541,247 bytes.
Public page/media/thumbnail/captions, video/chapter metadata, sitemap, robots and HTTPS redirect checks
passed; range request returned 206/1,024 bytes. Public browser playback and chapter seeking work.
Search Console requested sign-in, so Pages/Videos discovery reports remain unverified.
No YouTube/Instagram/Zernio posting.
