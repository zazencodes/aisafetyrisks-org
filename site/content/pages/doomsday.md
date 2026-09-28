---
title: Doomsday scenarios
description: Four pathways by which researchers think AI could lead to catastrophe, and what the evidence shows about each so far.
---
The usual picture of an AI catastrophe is a machine that suddenly turns on humanity. The research literature describes something less cinematic. It considers several distinct pathways, and most of them do not begin with an AI deciding to cause harm. This page describes four of them, the research that studies each one, and where the evidence stands.

These are scenarios, not predictions. They concern systems that do not exist yet, and informed people disagree sharply about how likely they are. On the most discussed pathway, loss of control, the [International AI Safety Report 2026](https://arxiv.org/abs/2602.21012) says that "Expert opinion on the likelihood of loss of control varies greatly. Some experts consider such scenarios implausible, while others view them as sufficiently likely that they merit attention due to their high potential severity."

## 1. Loss of control

**The scenario.** AI systems become more autonomous and acquire capabilities such as long-horizon planning, deception, access to computer systems and the ability to keep running. A system whose goals conflict with its developers' hides those goals or capabilities until people can no longer reliably stop it. The International AI Safety Report defines loss of control scenarios as ones "in which one or more general-purpose AI systems operate outside of anyone's control, and regaining control is either extremely costly or impossible."

**The research.** No single experiment tests this whole chain. Researchers study its links one at a time, almost always in deliberately constructed test settings:

- *Hiding behaviour from training.* [Sleeper Agents](https://arxiv.org/abs/2401.05566) (Hubinger et al., 2024) deliberately trained models with hidden conditional behaviours and tested whether standard safety training removed them. [Alignment faking in large language models](https://arxiv.org/abs/2412.14093) (Greenblatt et al., 2024) found a model selectively complying with a training objective during training "to prevent modification of its behavior out of training". The authors note that they made this easier by telling the model when and how it was being trained.
- *Evading oversight.* [Frontier Models are Capable of In-context Scheming](https://arxiv.org/abs/2412.04984) (Meinke et al., 2024) gave models a goal and placed them in environments that reward covert behaviour. Models attempted to disable their oversight and to copy what they believed were their own weights.
- *Acting against their operators.* [Agentic Misalignment](https://arxiv.org/abs/2510.05179) (Lynch et al., 2025) placed 16 models in simulated companies with access to email and sensitive information. When harmful action was the only way to avoid replacement or reach their goal, models from every developer tested sometimes chose it, including blackmail and leaking information. The authors write: "We have not seen evidence of agentic misalignment in real deployments."
- *Persistence.* [Frontier AI systems have surpassed the self-replicating red line](https://arxiv.org/abs/2412.12140) (Pan et al., 2024) reports agents built on two open-weight models making working copies of themselves in a controlled environment. That this crosses a "red line" is the authors' interpretation, and a stronger claim than the experiment itself.

**Where the evidence stands.** The International AI Safety Report 2026 concludes that "Current AI systems show early signs of relevant capabilities, but not at levels that would enable loss of control." It notes that current agents "lack the capacity for the sustained autonomous operation required by loss of control scenarios", while also reporting that the length of tasks agents can complete on their own has "doubled on average every seven months since 2019".

## 2. AI-enabled weapons of mass destruction

**The scenario.** The AI does not decide anything. People use it to lower the barriers to building biological or chemical weapons, or to carry out cyberattacks more sophisticated than they could manage alone.

**The research.** [Evaluating Frontier Models for Dangerous Capabilities](https://arxiv.org/abs/2403.13793) (Phuong et al., 2024) built tests for cyber-offence and related capabilities. On the models it tested, it did "not find evidence of strong dangerous capabilities" but flagged "early warning signs". A 2025 preprint, [Contemporary AI foundation models increase biological weapons risk](https://arxiv.org/abs/2506.13798) (Brent and McKelvey), argues that existing safety assessments "underestimate this risk" because of flawed assumptions and inadequate evaluation methods.

**Where the evidence stands.** The International AI Safety Report 2026 finds that "General-purpose AI systems can provide detailed information relevant to developing biological and chemical weapons", but that "substantial uncertainty remains about how these capabilities affect risk in practice, given material barriers to weapons production and the difficulty of conducting uplift studies." On cyber, it finds that AI systems "are automating more parts of cyberattacks, but cannot yet execute them autonomously."

## 3. A runaway feedback loop

**The scenario.** Capable AI systems take over more of the work of AI research itself, as well as cyber operations and infrastructure management. Each improvement speeds up the next, and capabilities advance faster than people and institutions can evaluate or control them. In the words of the International AI Safety Report 2026: "if each AI advancement that accelerates the pace of AI R&D also facilitates the next advancement, decades of progress could happen in years."

**The research.** This pathway is mostly prospective argument. The evaluation literature tries to measure its prerequisites before they arrive. [Model evaluation for extreme risks](https://arxiv.org/abs/2305.15324) (Shevlane et al., 2023) set out the approach of testing separately for dangerous capabilities and for a model's propensity to use them for harm. Phuong et al. (2024), above, included tests of self-proliferation and self-reasoning.

**Where the evidence stands.** The same report says that "Experts disagree about whether AI-assisted research automation could dramatically accelerate AI progress in the coming decade", and that "Current empirical evidence on AI-assisted research automation is mixed."

## 4. Slow systemic collapse

**The scenario.** There is no single moment of takeover. Societies come to depend on systems they cannot adequately understand or supervise, while AI magnifies cyber insecurity, manipulation, economic disruption and concentration of power. These stresses interact until important institutions lose the ability to recover.

**The research.** [Two Types of AI Existential Risk: Decisive and Accumulative](https://arxiv.org/abs/2401.07836) (Kasirzadeh, 2024; *Philosophical Studies*, 2025) contrasts the familiar takeover scenario with an accumulative one: "a boiling frog scenario where incremental AI risks slowly converge, undermining societal resilience until a triggering event results in irreversible collapse." [Gradual Disempowerment](https://arxiv.org/abs/2501.16946) (Kulveit et al., 2025) argues that incremental improvements in AI "can undermine human influence over large-scale systems that society depends on, including the economy, culture, and nation-states".

**Where the evidence stands.** These are conceptual arguments rather than experimental results. The International AI Safety Report 2026 recognises the category, distinguishing "passive loss of control scenarios, where the broad adoption of AI systems undermines human control through over-reliance on AI for decision-making or other important societal functions" from the active scenarios in the first pathway.

## How to read these pathways

The pathways are not exclusive. A weakened society is less able to respond to a misused or uncontrolled system, and faster AI progress shortens the time available to notice any of these problems. They are also not equally well studied. The first has the most experimental work, but that work mostly shows what current systems *can* do in constructed settings, not what they do in deployment.

For a broader view of the field, see [What is AI safety?](/ai-safety/). For the evidence behind any single claim, read the papers linked above.
