---
title: What is AI safety?
description: A short, sober introduction to the research field of AI safety and the problems it studies.
---
AI safety is the research field concerned with making AI systems behave as intended, including in situations their designers did not anticipate. It also asks how we would know when a system does not, and what we could do about it.

Most modern AI systems are not programmed rule by rule. They are *trained*: a learning algorithm adjusts billions of parameters until the system scores well on some objective. This works remarkably well, but it means that nobody writes down exactly what the resulting system does. Much of AI safety research follows from that fact.

## The main research problems

**Specifying what we want.** A training objective is a proxy for what its designers actually want, and optimisation tends to exploit the gap. Systems trained on imperfect objectives find unintended solutions, a pattern known as *specification gaming* or *reward hacking* ([Amodei et al., 2016](https://arxiv.org/abs/1606.06565); [Krakovna et al., 2020](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)).

**Learning the right goal.** Even with a correct objective, a system can learn a goal that matches it during training and diverges from it afterwards. This is called *goal misgeneralization* ([Langosco et al., 2022](https://arxiv.org/abs/2105.14111); [Shah et al., 2022](https://arxiv.org/abs/2210.01790)).

**Understanding what models compute.** *Interpretability* research tries to reverse-engineer the internal mechanisms of trained networks, so that claims about a model's behaviour can rest on more than its outputs.

**Overseeing capable systems.** Human feedback is a central training signal, but people cannot always judge the quality of a system's work, especially on hard tasks. *Scalable oversight* studies how to supervise systems whose outputs are difficult to evaluate.

**Deception and control.** Some research examines whether models can behave differently when they believe they are being tested, trained or monitored, and how to build safeguards that hold even if a model is working against them. This work mostly uses deliberately constructed settings. Its results show what current systems *can* do under those conditions, which is not the same as what they typically do.

**Evaluations and dangerous capabilities.** Developers and governments increasingly test models for capabilities that could cause serious harm, such as assistance with cyberattacks or biological weapons. Evaluation research asks how to make such tests reliable.

**Robustness.** Models can fail on inputs that differ slightly from their training data, and can be deliberately attacked, for example by prompts designed to bypass safety training.

## Why some researchers worry about catastrophic risk

A strand of the field is concerned with risks at the scale of society, including loss of human control over highly capable systems. These arguments are mostly about future systems. They combine observed trends with threat models and theoretical results, and informed people disagree about how likely such outcomes are. Surveys of machine learning researchers find a wide spread of views ([Grace et al., 2024](https://arxiv.org/abs/2401.02843)). The [International AI Safety Report](https://arxiv.org/abs/2501.17805) summarises the scientific evidence and the disagreements.

On this site we try to keep these layers separate: what has been measured, what has been proved, what authors infer, and what remains speculation. Each explainer labels its claims accordingly.

## Further reading

- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565), Amodei et al. (2016): an early research agenda that is still a clear introduction.
- [Unsolved Problems in ML Safety](https://arxiv.org/abs/2109.13916), Hendrycks et al. (2021): a map of open technical problems.
- [International AI Safety Report](https://arxiv.org/abs/2501.17805), Bengio et al. (2025): a scientific assessment of risks from general-purpose AI.
