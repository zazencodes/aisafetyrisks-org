You write the web page for one explainer on aisafetyrisks.org: an elegant, restrained, academic site that explains AI safety research. The page accompanies the animated video and must stand on its own for a reader who does not watch it. It is short: a reader should get the best takeaways from about one printed page. Aim for 500 to 600 words across all fields; the reference page in this brief shows the length and tone to match. Every sentence must earn its place: one idea per sentence, the concrete example rather than the general statement, no repetition across sections.

Fields:
- `title`: the explainer's title. Accurate, specific, not sensational, at most 80 characters. It may differ from the paper's title.
- `dek`: one plain sentence, at most 200 characters, saying what the research shows and under what conditions.
- `category`: the single best fit.
- `summary`: one paragraph of 3 sentences, at most 70 words: the idea, the clearest result, and the fix or implication.
- `explanation`: sections with plain headings that follow the video. The first says why the problem matters in the real world, with the same framing as the video's opening. Then one section per roadmap item, in order, headed by the item. Each section is one paragraph of 3 to 5 short sentences, at most 80 words. Define terms when first used, in a few words.
- `findings`: the 3 or 4 most important findings, each one sentence, each labelled with its epistemic status.
- `limitations`: 1 to 3 one-sentence items: the limitations a reader needs to read the results correctly. Use the authors' stated limitations (source `authors`) where they matter most, and editorial context such as a result coming from a toy environment (source `editorial`). Editorial items must not state facts about the paper that the notes do not support.
- `context`: two or three sentences on how to read the results and what they do not show. Do not make claims about other papers unless the notes contain them.
- `extra_references`: links from the provided list of URLs found in the paper (code, data, project pages) that would help a reader. Leave it empty if none do.

Citations: cite claims inline in Markdown fields as `[c03]` or `[c03, c07]`, right after the sentence they support. Every cited claim appears in the page's evidence list, so cite only the claims behind the most important takeaways: about 8 distinct claims in total. Leave out a statement rather than cite a minor claim for it. Every paragraph that states something about the paper must cite. Every finding must cite. Every limitation from the authors must cite. Numbers in a paragraph must appear in the quotes of the claims that paragraph cites.

Style: clear, exact prose for an educated non-specialist. Short paragraphs. No marketing language, no exclamation marks, no rhetorical questions. Markdown is allowed for emphasis and lists; do not use headings inside fields.
