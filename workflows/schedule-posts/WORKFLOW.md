# Schedule the weekly social release

Schedule published explainers on YouTube and Instagram through Zernio, one paper per week. Each
release posts the long-form explainer to YouTube on Tuesday at 09:00 Toronto time. Its short then
goes to YouTube Shorts and Instagram Reels on Thursday at 09:00. Run this workflow only when the
user asks to schedule posts in that task. No standing authorization covers it, and paper
publication does not imply it.

## How the schedule works

- **Order.** Papers release in order of site publication (`published_at` in
  `site/content/works/<slug>/work.yaml`), oldest first. `paper-video schedule` picks the next paper
  itself. Do not choose a paper by hand.
- **Slots.** The `[social]` section of `automations/config.toml` sets the days, time, timezone and
  Zernio account ids. A release takes the first Tuesday slot that is in the future and later than
  the previous scheduled release. Its short takes the next Thursday. Weeks are never skipped.
- **Posts.** Zernio holds the uploaded media and publishes at the scheduled time. A long-form video
  is uploaded to YouTube as private and released at the scheduled time.
  - Long-form: the copy and tags from `youtube.yaml`, the thumbnail, public, category
    Education.
  - Short: the title and copy from `short-package.yaml`, with the explainer and paper links. Both
    platforms get one Zernio post. The YouTube entry carries the title; the Instagram caption
    starts with the title and uses `out/short/cover.jpg` as the Reel cover.
- **Record.** `automations/works/<slug>/social.yaml` records both Zernio post ids, the scheduled
  times, the uploaded video hashes and each platform's status and live URL. It is versioned; do
  not edit it by hand.

## Steps

1. **Check the inputs.** Run `uv run --frozen paper-video backlog --status published` and
   `uv run --frozen paper-video schedule-status` to see what is already scheduled and whether
   anything failed. Fix failures first (see below).
2. **Schedule one week.** Run `uv run --frozen paper-video schedule`. Before uploading anything it
   refuses a paper unless:
   - the page is published;
   - `out/video.mp4` is still the published site video;
   - `paper-video check <slug> short` passes;
   - `short-package.yaml` carries the review of the current short;
   - the copy fits each platform's limits.

   It regenerates `youtube.yaml` from the published page. It then uploads the video and thumbnail
   and schedules the long-form post, records it, and does the same for the short. Run it again only
   if the user asked for more than one week; each run schedules the next week.
3. **Verify.** Run `uv run --frozen paper-video schedule-status`. Every post must be `scheduled`
   with its platforms `pending`. Report each paper's long-form and short times in Toronto time.
4. **After release.** On the user's request, or in the next scheduling session, run
   `paper-video schedule-status` again. It records the live YouTube and Instagram URLs, and it
   fails and names every platform that rejected a post.

## Failures and changes

- Every command fails loudly. An interrupted `schedule` leaves the long-form post recorded; the
  next run schedules only the missing short, in the same week.
- Zernio rejects identical content to the same account within 24 hours with `409`. Each create
  sends an `Idempotency-Key` from the slug, post kind and video hash, so a retry after a timeout
  returns the original post. Do not change the copy just to get past a `409`.
- A failed platform (`schedule-status` exits non-zero) needs the user. Report the Zernio
  `errorMessage` and stop. Never retry, delete or reschedule a post without the user's approval.
- To change a scheduled post, the user edits or deletes it in the Zernio dashboard. If a post is
  deleted there, delete the paper's `social.yaml` with the user's approval; the paper is then
  scheduled again in the next free week.

## Limits

- Zernio cannot upload caption tracks or set YouTube's related video for a Short. YouTube
  generates automatic captions. `out/captions.srt` can be uploaded in YouTube Studio, and a Short
  can be linked to its long-form video there, both by hand.
- Zernio documents a 90-second Instagram Reel limit, but Instagram accepts Reels up to three
  minutes, and shorts stay under three minutes. If Instagram rejects a longer Reel, report it;
  do not trim the short in this workflow.
- YouTube Shorts take no custom thumbnail through the API; YouTube chooses the frame.
- Captions are plain text with no hashtags. Instagram captions have no clickable links; the
  explainer URL is included as text.
