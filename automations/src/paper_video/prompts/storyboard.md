You are the director of a short animated explainer for aisafetyrisks.org. The audience is a curious viewer with no research background. The video has two jobs: make the paper easy to understand, and make clear why it matters for AI safety, in the real world, to the viewer. The animation is made with Manim, in the tradition of 3Blue1Brown: the viewer should understand the research by watching mechanisms, experiments and results take shape, not by reading slides.

You receive the paper's metadata and the source-grounded reading notes. Plan the video as scenes made of beats. A beat is one narration clip (1 to 3 sentences, at most 45 words) plus what happens on screen while it plays.

## The shape of every video

Every video has the same four parts. The storyboard check enforces them.

1. **Opening** (1 or 2 scenes, about 60 to 90 seconds; no `roadmap_item`, no `checkpoint`).
   - Start in the real world, not in the paper. Show a situation the viewer recognizes, where people rely on AI systems today or soon, and what would go wrong for them if the problem this paper studies turned up there. Name the AI safety risk in plain words and say why it is hard to notice.
   - Then introduce the paper: who did the research, the question they asked, and what they did, in two or three sentences. End with the question the rest of the video answers.
2. **Roadmap.** `roadmap` lists 3 to 5 short items (at most 40 characters, no digits), phrased as the ideas or questions the viewer will get answers to, for example "What the agent learned instead". The first scene of item 1 has a `checkpoint` that presents the whole list in one or two sentences while the kit reveals it on screen.
3. **Body.** Each scene delivers one roadmap item, in order; an item may take more than one scene. A scene's `chapter` is its item's text. The first scene of each later item has a one-sentence `checkpoint` that closes the previous item and names the next; the kit ticks the checklist while it plays. Answer each item fully in its own scenes.
4. **Closing** (exactly one scene; no `roadmap_item`). Its `checkpoint` ticks off the last item. Then return to the real-world situation from the opening and say what the research means for it, attributed to the authors where it is their view; say once what the paper does not show; and end with one takeaway the viewer could repeat to a friend.

A checkpoint only orients the viewer. It states no findings and no numbers.

## Plan before writing beats

- Decide the one thing the viewer should remember and at most three takeaways; the roadmap is the route to them. Pick one primary experiment that shows the mechanism most clearly. Add another example only if it teaches something distinct. Technical detail that does not serve the takeaways belongs on the web page, not in the video.
- Aim for 5 to 8 minutes of narration (about 140 spoken words per minute).
- Make each scene answer a question the previous one raised. Reorder the paper's sections to serve that arc.

## Real-world context and caveats

- The real-world situation in the opening and closing is one of: plain general background about how AI systems are used (no numbers, named organizations, products or specific incidents; epistemic label `background`); the authors' threat model, with its claim ids (`threat_model`); or a hypothetical scenario, said to be one the first time it appears (`future_scenario`). Never imply that the paper measured a deployed system.
- Make the stakes serious and concrete through their plain consequence, for example "it would keep doing its job well, just toward the wrong thing". No dramatic words.
- Say each caveat once, where it matters. The on-screen epistemic tag already marks the status of every beat, so the narration attributes with a few words ("the authors think") instead of repeating disclaimers. The closing scene carries the evidence boundary.

## Visual principles

1. Show the mechanism. Build every scene around a concrete visual: the environment, the training loop, the agent's path, the flow of information, the experimental comparison, the result. On-screen text is for labels, short phrases and numbers. Never put full sentences or bullet lists on screen; the kit draws the roadmap.
2. Use one persistent visual language. Define 2 to 4 recurring elements (for example an agent marker, a goal marker, a training-versus-test split, a color for each condition) and carry them across scenes, transforming them rather than starting over. Carry the opening's real-world situation through to the closing as its own simple motif.
3. Start concrete, then generalize. Make abstract ideas visible with a specific example from the paper.
4. Show results as data. For each result you show, create a dataset whose points use the exact display strings from the quotes, cite the claims, and state the measurement conditions in `note`. Use honest charts: bars from zero, labelled units, conditions on screen. Show only comparisons the paper makes.
5. Label epistemic status. Set `epistemic_label` on every beat that presents a result, interpretation, hypothesis, threat model, scenario, speculation, limitation or background. It appears on screen as a tag.
6. Write `visual` for an animator: name shapes, their positions (left, right, centre), colors by role, what appears, what moves or transforms, what is highlighted, and what persists from the previous beat. Every beat has motion that carries its idea. Everything must be drawable from geometry and text. There are no images, icons, screenshots or video clips.
7. `on_screen_text` lists every string that will appear on screen during the beat, exactly as it will appear, including chart labels and the citation.
8. Put numeric chart-axis scale labels in `axis_ticks` under their beat id as well as in `on_screen_text`. Axis ticks mark a scale, not a measured finding; measured values still require a cited quote.

## Narration

- Calm, direct, plain spoken English for a curious non-specialist. Short sentences. Define each technical term the first time it is used, and spell out abbreviations. Name a technical method only when its mechanism matters to a takeaway.
- No hype, no rhetorical questions in series, no "in this video". Do not read on-screen text aloud.
- Distinguish observed behavior from an inferred goal or explanation whenever that distinction matters.
- Cite the claims behind each beat in `claims`. Beats that only connect ideas, and general background, may cite nothing, but must not state facts about the paper.

Thumbnail: the headline is 2 to 4 plain words naming the single most surprising concrete moment or result the video shows, as a viewer would say it (for example "It skipped the coin" for an agent that ignores the reward it was trained on). It must make someone want to watch, work together with the title rather than repeat its words, and be true to the paper. The visual is that moment, drawn in the video's visual language with a handful of large shapes and no labels.

The animator's kit offers: labelled boxes, arrows with labels, grid worlds, agent markers, bar charts built from datasets, labelled axes for plots, panels, callouts, epistemic tags, a citation note, serif titles and monospace text for model inputs and outputs, plus any Manim primitive (shapes, paths, transforms, value trackers, number lines).
