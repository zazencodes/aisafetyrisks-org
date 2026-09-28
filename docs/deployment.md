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
subagent prompts, science review prompts, and correction rules. Its normal endpoint is a
draft for human review. Continue with approval and deployment only when the user explicitly
authorizes them. Additional science review rounds beyond its limits also need authorization.

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
5. With explicit user authorization, approve:

   ```sh
   uv run --frozen paper-video approve <slug>
   ```

   Approval rechecks page provenance and current science reviews, rejects unresolved blocker
   or major issues, uploads the mirrored video to R2, marks the page published, records the
   human review date, and updates the backlog. Minor issues can remain and must be reported.
6. Deploy the site:

   ```sh
   cd site
   npm run deploy
   ```

   Wrangler rebuilds the site before uploading it. Record the successful deployment's
   version ID. This publishes all current site content and static assets in the workspace.

To deploy a site-only change after authorization, use step 6. If changing a published paper's
content or media, repeat the applicable generation/review steps and approval first.

## Verification and failure recovery

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
