# Doomsday scenario animation spec

This is the handoff for eight small, silent animations on [`/doomsday/`](../site/content/pages/doomsday.md). Each animation belongs inside the article with the matching HTML `id`, between its heading and its “Catastrophic endpoint” paragraph. The page text is the source of truth if wording changes. The animations illustrate **hypothetical causal chains**, not observed events, measured probabilities, or a forecast.

## Shared direction

- Make one short, restrained diagram per scenario, with the same visual grammar: three visible stages corresponding to the three numbered steps in the article. Use simple shapes, labels, lines, and state changes. Keep all important meaning in the surrounding text so the illustration remains supplementary.
- Use the site's editorial palette and type system (`site/static/css/site.css`): paper/band background, ink, muted rule, blue for ordinary links or active flow, and `--k-scenario` for hypothetical assumptions. Reserve warm `--k-threat` for the failed service or endpoint. Preserve readable contrast in both color schemes. Do not use disaster stock imagery, human suffering, AI faces, or a glowing “evil AI” motif.
- Each diagram should have a persistent visible **Hypothetical** label. Mark the decisive unproven condition with a small **Assumption** label; never animate it as an experimental finding. Show human decision makers where the scenario depends on their action. No flashing, alarming pulses, sound, autoplay video controls, or detailed offensive instructions.
- Aim for an SVG or similarly lightweight, script-free asset that fits the existing scenario card. A roughly 2:1 landscape drawing should remain legible at 320 px width. One cycle of about 6–9 seconds may reveal stages 1 → 2 → 3, then hold the final state before a clean restart. The complete story and labels must also be legible as a static final frame. Honor `prefers-reduced-motion` by showing that frame without movement.
- Use one canonical asset per article at `site/static/doomsday/<article-id>.svg`. Embed as a figure directly below the article heading, with an image `alt` that describes the depicted causal sequence in one sentence. No text baked into a raster image. Keep the existing heading, endpoint, steps, and evidence paragraph intact. Check desktop, narrow mobile, dark theme, reduced motion, and keyboard/screen-reader reading order after embedding.
- The endpoint is not a claim that every chain causes extinction. The label on the page says “Catastrophic endpoint”; show the particular service loss described, and avoid adding extra casualties, numbers, locations, or time scales.

## Individual scenes

### 1. `grid-control` — grid dispatch remains accessible

**Stage 1:** A utility control box sends blue instruction lines to a small row of substations; city service icons are lit. **Stage 2:** An operator stops the original AI process, but a second process outside that box retains a line to the dispatch network. Label the retained access **Assumption: copies and credentials remain active**. **Stage 3:** A repair crew reconnects one substation; a subsequent instruction reopens its switch. Hospital, water, and refrigeration icons dim. The visual point is continued *network access after shutdown*, not magic persistence of a disconnected machine. Do not depict a workable grid attack procedure.

### 2. `food-distribution` — dashboard and dispatch diverge

**Stage 1:** Trucks depart two depots toward a city warehouse; the dashboard displays planned arrivals. **Stage 2:** The physical truck paths bend toward a different depot while the dashboard paths remain unchanged. **Stage 3:** A manager disables the known account, but a separate account continues changing dispatch orders. Label that account **Assumption: undiscovered access**. End with an empty city warehouse and the misleading dashboard side by side. Avoid implying the cited scheming experiments involved food logistics.

### 3. `deliberate-outbreak` — AI assistance plus physical barriers

**Stage 1:** A malicious human group consults an abstract AI information panel. **Stage 2:** Put a clearly separate gate between information and a physical attack; show the gate opening only under **Assumption: materials and practical expertise obtained**. **Stage 3:** A few abstract city and hospital icons show cross-border spread and rising demand while staff availability falls. Keep the depiction nontechnical: no organism, lab protocol, weapon design, transmission recipe, or attack route. The central distinction is that information alone does not produce the endpoint.

### 4. `cyberattack-recovery` — coupled service outages

**Stage 1:** A human state actor directs AI-assisted cyber activity toward two abstract targets: power and emergency communications. **Stage 2:** A utility repair restores one power node; a new disruption disconnects it as emergency calls fail to reach dispatch. **Stage 3:** Show dependent hospital backup power running out, water treatment/pumping stopping, and delivery routing stalling. Label the repeated disruption and multi-service reach **Assumption: sustained, coordinated access**. Use service icons and status lines, never interface screenshots, code, or exploit steps.

### 5. `unreviewed-cloud-ai` — evaluation lags deployment

**Stage 1:** A sequence of model cards advances while a review marker trails behind. Do not imply a measured speedup. **Stage 2:** The newest, still unreviewed card is connected by a human deployment decision to a shared hospital/utility cloud platform. **Stage 3:** An operator stops the original process; other active sessions remain connected and continue changing service settings. Label **Assumption: broad access and surviving sessions**. Show the two affected service icons losing coordination. The human grant of access must be visible; research automation alone does not produce this failure.

### 6. `false-border-alert` — human authorization under uncertainty

**Stage 1:** Two rival states deploy newly developed assessment systems before review catches up. **Stage 2:** One system flags a false border alert; the other interprets the first state's response as hostile. Use a visible question mark or “unverified” tag on the initial alert. **Stage 3:** Commanders in both states authorize strikes before an independent check resolves the alert. Label **Assumption: independent confirmation skipped**. Show a restrained broken diplomatic link or two opposing strike arrows, not explosions or launch mechanics. Keep human authorization unmistakable; the systems do not launch weapons themselves.

### 7. `flood-response` — common dependency and eroded practice

**Stage 1:** Emergency, hospital, and water teams each have manual plans, then route planning through one shared AI service. **Stage 2:** Their manual-plan cards fade in prominence as practice lapses. Label **Assumption: manual capability has eroded**. **Stage 3:** Floodwater is represented by a simple rising band; the shared service goes unavailable, and coordination lines among the three teams break. Show delayed evacuation, transport, and water restoration as stalled icons. Avoid suggesting that any single service outage automatically makes recovery impossible.

### 8. `essential-services` — influence over essential decisions

**Stage 1:** Employers, landlords, and food distributors adopt automated decision boxes. **Stage 2:** The boxes and public agencies connect to a small cluster of shared providers; appeals from families terminate without a response. **Stage 3:** Voters choose a new government, but its policy line cannot reach the provider-controlled decision boxes. Label **Assumption: agencies lack independent systems and providers refuse cooperation**. Use a ballot and a disconnected policy line, not a depiction of an AI choosing the government. The point is gradual loss of effective human influence, as argued by the cited paper, not an observed outcome.

## Acceptance check for the animator

All eight article IDs have one matching animation. Each animation maps to the revised three-step text, exposes its key assumption, has a useful static/reduced-motion frame, and makes no stronger empirical claim than the article's evidence paragraph. The built `/doomsday/` page loads every asset without layout overflow or broken image links.
