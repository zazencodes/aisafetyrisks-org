# Independently review the short

You did not write this edit. Review the actual selected narration, headings, scope label, title,
description, cuts, captions and images, not merely the full video's original science review.
Write only short-review.yaml. Do not edit the plan or source materials.

Review the science against the supplied notes. Check whether deleting context changes a claim,
whether an illustrative scenario is mistaken for an experiment, and whether all experimental
conditions and central limitations survive. Check that the hook and takeaway are supported,
every antecedent exists in this edit, and the short clearly says what the paper did.

Inspect the contact sheet, individual frames and additional frames around any questionable cuts.
The sheet shows every cut's first frame, +0.3, +0.6 and +1 seconds and the segment end at phone
width. Text that morphs or overlaps mid-transition, even briefly and also inside a beat, is a major
issue. So is a frame of the next or previous beat at either edge of a cut, and a label or motion
that says more than, or contradicts, the narration. Extract frames with single `ffmpeg` commands;
do not wrap commands in `bash -c` scripts or delete files.
Look at phone size as well as full resolution. Check for truncated captions, overlapping text,
unreadable key diagram labels, missing source context, and visual states inherited from omitted
beats. Inspect the very first frame of every cut and the following transition; do not accept
unexplained labels from omitted beats merely because they disappear a second later. At
360-pixel phone width, check essential diagram labels for readability and sufficient contrast.
Verify box counts and chart labels/values against the notes. Caption batches must have at most two lines and use the same off-white ink throughout.
Check bold and italic phrases individually against the complete narration: they should guide
understanding, preserve negations and conditions, and avoid arbitrary dates or dramatic keywords.
Check that ordinary context can remain plain and that emphasis is sparse across the edit.
Inspect styled text for clipping, and ensure italics and bold remain legible at phone size.
Burned captions change at word timings read from the narration audio; flag cues that still
drift from the speech. Compare the selected WAV narration
lengths and edit timeline to ensure words are not cut. Listen to or play the video when tools allow;
if playback is unavailable, record that review limitation as a minor visual issue rather than
claiming that you watched or listened to it.

`science` is the ordinary ScienceReview; `visual_issues` uses the source beat ids. Set science.verdict
to accurate only when there are no blocker or major science issues. Report minor issues candidly.
The content_key ties your review to this exact edit, its source assets, and renderer.
