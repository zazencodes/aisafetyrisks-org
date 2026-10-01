# Edit one short from the completed explainer

Write exactly one self-contained portrait companion to this paper's full explainer. Choose the
edit only after the full video is assembled. The source is the completed storyboard and its
verified notes, not fresh research or your memory. Aim for 90–150 seconds; the actual whole-beat
duration must be strictly less than 180 seconds. Never speed up narration to make it fit.

Choose complete source beats, identified by beat id. The command reuses their narration and
animations verbatim, removes unselected beats and roadmap checkpoints, and lays out the whole
landscape diagram inside a 1080x1920 frame with large headings and burned-in captions.
Read all selected narration in its new order: every pronoun, "now", "second", and "that" needs
an antecedent in the short itself. Earlier visual state can persist inside a source scene; inspect
it at the cut and ensure it makes sense without the preceding beats. Include the setup if needed.

Give the short a concrete hook, a plain account of what the paper did, its central explanation,
an explicit limitation, and a useful takeaway. A narrow central mechanism is often enough;
explain the paper's main scope without promising the entire long video. For a research agenda,
say that its experiments are proposals. Keep model/environment conditions attached to empirical
results. A hypothetical robot example must remain hypothetical. The limitation must be spoken,
not only written in the description. Remove details to shorten; keep the conditions and caveats.

`title`, `description`, `scope_label`, and each segment's `heading` are visible editorial copy and
must meet the same scientific integrity rules as the narration. Support them with the selected
beats' claim ids. Headings have room for two lines; keep them brief. The persistent scope_label
names the setting or epistemic status (for example "Research agenda · hypothetical examples").
The command adds the paper citation, explainer URL, source URL, and website call to action.
For each segment, write `caption_emphasis` as a list of objects with `phrase` (exact narration
text) and `kind`: `emphasis` for amber yellow, or `harm` for the animation palette's orange-red.
Use yellow for ordinary emphasis on mechanisms, conditions and caveats; use orange-red for
harms, failures and dangerous behavior. Use [] when emphasis adds nothing. Do not rewrite words.
Emphasis uses the main IBM Plex Sans Medium font and remains attached to the phrase across
caption cues and line breaks. Phrases must match the source exactly and must not overlap.
Each caption batch has at most two lines and one accent color alongside the white base text.
The renderer splits batches at color changes and measured line limits, preserving every word.
Do not add marketing claims, unrelated account links, or instructions to post the content.

In `selection_reason`, explain why this edit works on its own and which long-form material was
removed. Select a hook first, a takeaway last, and at least one context, explanation and limitation
beat. Record each segment's narrative role; the roles are for checking the edit, not on-screen copy.

If the completed explainer lacks whole beats that make an accurate, self-contained short, improve
its storyboard and scene code through the publish-paper workflow, reassemble it, and select the
new beats. Do not silently splice sentences, rewrite narration over mismatched animations, crop
away conditions, or produce a placeholder short.
