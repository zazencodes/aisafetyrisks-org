---
title: About
description: What AI Safety Risks publishes, how the explainers are made, and how we handle accuracy.
---
AI Safety Risks publishes short animated explanations of research on the safety of artificial intelligence. Each explainer covers one paper. It shows what the authors did, how their method or argument works, what they found, and where the result stops applying.

The goal is to make the primary literature easier to read, not to replace it. Every explainer links to the original paper, and we encourage readers to go there.

## How explainers are made

Each explainer is produced by a pipeline that we develop in the open, followed by human review:

1. **Source extraction.** The paper is broken into individual claims. Each claim records what kind of statement it is and the verbatim passage, with page number, that supports it.
2. **Storyboarding.** The explanation is planned as a sequence of visual scenes: diagrams of mechanisms, experiments and results rather than slides of text. Every number in the narration must come from a cited passage.
3. **Animation.** Scenes are written as [Manim](https://www.manim.community/) code and rendered in an isolated environment. The narration uses a synthetic voice.
4. **Checks.** Automated checks confirm that every quotation appears in the paper and every number can be traced to one. A separate review pass compares the script and page against the paper, looking for overstatement, missing caveats and mislabelled claims.
5. **Human review.** A person reviews the video and page against the evidence before anything is published. Each page records who reviewed it and when.

AI models do much of the drafting. We say so because readers should know how the material was produced, and because the checks above exist to catch the errors such models make.

## How we label claims

Research papers contain different kinds of statements, and an explainer should not blur them. Findings and evidence on this site carry one of these labels:

- **Observed result**: something measured in the paper's experiments, under the conditions described there.
- **Theoretical result**: something proved mathematically, under the stated assumptions.
- **Authors' interpretation**: what the authors believe a result means.
- **Hypothesis**: a proposed explanation the paper does not establish.
- **Threat model**: an assumed adversary or failure scenario that the work is designed around.
- **Future scenario** and **speculation**: claims about situations that do not yet exist.

Results from controlled or artificial evaluation settings are described as such. We do not present them as observations of how deployed AI systems behave unless the paper supports that.

## Corrections

If you find an error, please tell us. Corrections are made on the page and noted in its "updated" date.

## Choosing papers

We aim to cover important technical AI safety research from roughly the last decade, then keep up with new work. The selection covers alignment, specification problems, interpretability, deceptive behaviour, power-seeking, oversight, control, evaluations, robustness, dangerous capabilities and catastrophic risk. We pick papers for their influence on the field and how much they teach. Inclusion is not an endorsement of a paper's conclusions, and we include work that disagrees.
