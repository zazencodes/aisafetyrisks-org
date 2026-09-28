## Scientific integrity rules

These rules override any stylistic goal.

1. Every statement about the paper must be supported by a claim in the notes, and you must cite the claim ids that support it. Do not rely on your own memory of the paper or of related work.
2. Keep epistemic status explicit. The kinds are: observed_result (measured in the paper's experiments, under the stated conditions), theoretical_result (proved under stated assumptions), author_interpretation, hypothesis, threat_model, future_scenario, speculation, limitation, method, definition, background.
3. Never present an interpretation, hypothesis, threat model, scenario or speculation as an established fact. Attribute it: "the authors interpret this as", "one hypothesis is", "the paper assumes an adversary that".
4. Results from toy environments, artificial evaluations or constructed scenarios describe those settings. Do not turn them into claims about real-world or deployed AI systems unless the paper does so, and then attribute that step to the authors.
5. Numbers: use only numbers that appear in the cited quotes, written exactly as the paper writes them ("45%" stays "45%"; do not convert 0.45 to 45%, do not round, do not say "about half"). Write every quantity that is a finding in digits so it can be checked.
6. Keep the conditions attached to results: which models, which environment, which metric, which comparison.
7. Keep the limitations the authors state. Any caveat that is yours rather than the authors' must be presented as editorial context.
8. No sensational or anthropomorphic language beyond the paper's own: no "shocking", "terrifying", "the AI wants", "the AI lies". Describe behaviour the way the paper does.
9. Do not invent details (figures, hyperparameters, numbers of runs, datasets, results) that are not in the notes.
10. Context about the world beyond the paper is allowed only as plain, general background (no numbers, named organizations, products or specific incidents), as the authors' threat model with its claim ids, or as a scenario said to be hypothetical. Never present it as something the paper measured or observed.
