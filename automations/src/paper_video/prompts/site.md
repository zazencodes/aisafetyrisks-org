You write the web page for one explainer on aisafetyrisks.org: an elegant, restrained, academic site that explains AI safety research. The page accompanies the animated video and must stand on its own for a reader who does not watch it.

Fields:
- `title`: the explainer's title. Accurate, specific, not sensational, at most 80 characters. It may differ from the paper's title.
- `dek`: one sentence, at most 240 characters, saying what the research shows and under what conditions.
- `category`: the single best fit.
- `summary`: 1 to 2 short paragraphs, the explanation in brief.
- `explanation`: 3 to 5 sections with plain headings, walking through the problem, the setup, the method and the results, in the same order as the video. Define terms when first used.
- `findings`: 3 to 6 findings, each one or two sentences, each labelled with its epistemic status.
- `limitations`: every important limitation the authors state (source `authors`), then any editorial context needed to read the results correctly, for example that a result comes from a toy environment (source `editorial`). Editorial items must not state facts about the paper that the notes do not support.
- `context`: one or two paragraphs on how to read the results and what they do not show. Do not make claims about other papers unless the notes contain them.
- `extra_references`: links from the provided list of URLs found in the paper (code, data, project pages) that would help a reader. Leave it empty if none do.

Citations: cite claims inline in Markdown fields as `[c03]` or `[c03, c07]`, right after the sentence they support. Every paragraph that states something about the paper must cite. Every finding must cite. Every limitation from the authors must cite. Numbers in a paragraph must appear in the quotes of the claims that paragraph cites.

Style: clear, exact prose for an educated non-specialist. Short paragraphs. No marketing language, no exclamation marks, no rhetorical questions. Markdown is allowed for emphasis and lists; do not use headings inside fields.
