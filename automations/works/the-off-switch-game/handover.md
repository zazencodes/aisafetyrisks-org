# Draft handover

The Off-Switch Game is ready for human review. It remains in_progress in the backlog; nothing was approved, uploaded or deployed.

## Deliverables

- out/video.mp4: 358.1 seconds, 1920×1080, 60 fps, H.264 video and AAC audio.
- out/thumbnail.jpg
- out/captions.vtt and out/captions.srt
- youtube.yaml: upload package
- site/content/works/the-off-switch-game/work.yaml (relative to repository root): draft page

Preview: `uv run --frozen aisr-site serve --drafts --media-root automations/media`

A preview was started on port 8765: http://localhost:8765/works/the-off-switch-game/

## Validation

33 notes claims have verified source quotes. Storyboard and page provenance checks pass. Independent science reviews of both current artifacts are accurate, with no open issues. All scenes have current visual reviews and zero automated layout problems. Site draft build and git diff whitespace checks pass. Browser verification confirmed video playback, chapter seeking, English caption track, and correct local hashed media source.

Read captions.vtt in full: the risk is introduced by 00:35 and the paper's method by 00:54; the three roadmap items are answered in order; the closing returns to the hypothetical delivery robot and states the model boundary. No narrative-shape failure found.

Visual review used every scene's beat contact sheet plus the thumbnail at 320×180. Browser playback was spot-checked, not watched or listened to end-to-end; full audiovisual and pronunciation review remains for the human reviewer.

## Open minor issues

- Audience, s04b03–s04b04: the cost of excessive uncertainty remains abstract; a concrete example could improve comprehension.
- Visual, s05b02: the repeated Human feedback label becomes small in the reduced overview; hiding this repeated label would resolve it.

No blocker or major issues remain.
