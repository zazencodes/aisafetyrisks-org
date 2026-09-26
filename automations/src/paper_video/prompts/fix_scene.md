## Render, check and fix

Render with the command given below. It checks the file against the hard rules, renders it with the workspace's Manim installation, and checks the layout at the end of each beat. Then inspect the contact sheet, write `visual-reviews/<scene>.yaml` with the render key and any issues, and re-run the command to record the review. The result is printed and saved to the scene's check file.

- The file is rejected: fix every listed problem.
- The render fails: read the error at the end of the log and fix the cause.
- Layout problems (text overlapping or cut off, animations longer than the narration): fix every one.
- Visual review issues of severity blocker or major: fix every one. Minor issues are optional.

Keep what works and change only what fixes a problem. Re-render and update the keyed visual review after each fix. Stop when the file renders with no layout problems and no blocker or major visual issues, or after 4 fix rounds; then report what is still wrong.
