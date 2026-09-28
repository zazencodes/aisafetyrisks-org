## Render, check and fix

Render with the command given above. It checks the file against the hard rules, renders it with the workspace's Manim installation, and checks the layout at the end of each beat. Then inspect the contact sheet, write `visual-reviews/<scene>.yaml` with the render key and any issues, and re-run the command to record the review. The result is printed and saved to the scene's check file.

The contact sheet shows one frame per beat, captured at the end of the beat and labelled with its id; a checkpoint frame shows the kit's roadmap. Review it for concrete defects only:
- text overlapping text or shapes so that it is hard to read; text cut off by the frame; text too small or low-contrast;
- clutter: too many elements, crowding at the edges, unbalanced composition;
- a frame that does not show what the beat's `visual` asks for, or leftover elements from an earlier beat that no longer belong;
- a beat whose frame shows nothing new although its `visual` asks for a change;
- a chart or diagram that could mislead: truncated axes, unlabelled values or units, misaligned labels;
- a missing epistemic tag when the beat has an `epistemic_label`;
- blank or nearly blank frames where content is expected.

Severity: blocker (unreadable, wrong or misleading), major (clearly unpolished or confusing), minor (small refinement).

- The file is rejected: fix every listed problem.
- The render fails: read the error at the end of the log and fix the cause.
- Layout problems (text overlapping or cut off, animations longer than the narration): fix every one.
- Visual review issues of severity blocker or major: fix every one. Minor issues are optional.

Keep what works and change only what fixes a problem. Re-render and update the keyed visual review after each fix. Stop when the file renders with no layout problems and no blocker or major visual issues, or after 2 fix rounds; then report what is still wrong.
