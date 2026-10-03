# Paper influence and later context

Every published explainer has `site/content/works/<slug>/impact.yaml`. This file is the
canonical source for “Why this paper matters today”; `paper-video site` preserves it because
it regenerates only `work.yaml` and the explainer assets. Drafts can be previewed before their
impact section is ready. A production build refuses a published page without this file.

The section is editorial context about later work. It does not change the original paper's
claim register or imply that the original authors measured the later results. Each example
has a primary-source link, a short description of the relationship, and a verbatim supporting
`source_passage` for editorial review. Distinguish direct extensions and replications from
related research; include limitations or challenges where relevant. The summary synthesizes
the linked examples. Do not infer causal influence from a shared topic alone.

Use the year of the work's original publication, rather than the upload date of a later
copy. For example, *Concrete Problems in AI Safety, Revisited* was published at an ICLR
workshop in 2020, though its arXiv copy was submitted in December 2023.

`updated_at` records the actual editorial update with its time zone. The build uses the
later of this timestamp and the explainer's own update timestamp for Article `dateModified`
and sitemap `lastmod`. It preserves the original publication date and VideoObject `uploadDate`.
Unchanged builds never update these timestamps.

## Citation snapshots

The publishing workflow requires researching and supplying the best available citation count.
The schema permits an absent count for unfinished drafts; this is not a completed citation
research step. Use a traceable, manually verified snapshot, starting with OpenAlex. Record
`count`, the exact record URL and title, `retrieved_on`, and the indexed version's `scope`.
Verify identity using title, authors, DOI, publication information and full-record locations.
Check original-PDF links and alternate publication versions before rejecting a record based
on its headline date or title. OpenAlex often attaches the wrong title or abstract to arXiv
records: when the author list and the arXiv location or DOI match the paper, the record is the
paper, whatever its displayed title. Use that record and say so in `scope`. If the DOI lookup
fails, filter by arXiv location
(`/works?filter=locations.landing_page_url:http://arxiv.org/abs/<id>`), then search by title
and author, and consult
other citation indexes when necessary. Ensure the rendered provider name matches the source;
the current template labels snapshots as OpenAlex, so a different provider requires updating
that attribution before publication.

A verified reprint or combined-version count is acceptable: imperfect coverage is preferable
to omitting a usable, attributable count. Explain what the count covers instead of requiring
an exact original-version total. A failed first lookup is not grounds for publishing
“Citation count unavailable”. If a thorough search produces no defensible count, flag the
citation research as unresolved publication work rather than silently completing the step.

Do not sum preprint and conference versions: citations may overlap. Do not treat a missing
or mismatched record as zero citations. Counts indicate indexed attention, not endorsement
or correctness. They are rendered from content; visitors do not trigger external API calls.

For a refresh, retrieve the verified record at `https://api.openalex.org/works/<OpenAlex ID>`,
check its identity again, and update the snapshot and editorial timestamp only when the
content changes. Review newer research at the same time, then run the deployment checks.

## Initial research, 3 October 2026

All seven published explainers received two primary-source examples. Counts were retrieved
from the OpenAlex API and verified for:

- The Off-Switch Game: `W2558801266`, 84, IJCAI 2017 version.
- Goal Misgeneralization in Deep Reinforcement Learning: `W4287164755`, 21, arXiv version.
- Alignment faking in large language models: `W4405627013`, 27, arXiv version.

Counts were omitted for the remaining four papers:

- The Basic AI Drives: the title/author match was a 2018 book chapter, rather than the
  original 2008 paper.
- Concrete Problems in AI Safety: the arXiv DOI lookup returned 404; title search did not
  return a verifiable original-paper record.
- Frontier Models are Capable of In-context Scheming: the DOI lookup returned a record
  titled “AI and the End of an Era”.
- Stress Testing Deliberative Alignment for Anti-Scheming Training: the DOI lookup returned
  a record titled “Base-Axiom Initialization for Deliberative Alignment - A qualitative
  approach to Stress Testing Deliberative Alignment for Anti Scheming Training -”.

The later-paper links and supporting passages are retained in the individual impact files.

## Mislabelled arXiv records: corrected verification

The first pass rejected three papers only because of their OpenAlex titles. Their author lists
and arXiv locations match, so counts were added on 3 October 2026:

- Concrete Problems in AI Safety: `W2462906003`, 1,368. It is titled "Agnostic Learning with
  Unknown Utilities", has an unrelated abstract and lists unrelated DOIs; the scope says the count is approximate.
- Frontier Models are Capable of In-context Scheming: `W4405173927`, 21.
- Stress Testing Deliberative Alignment for Anti-Scheming Training: `W4414697811`, 2.

## The Basic AI Drives: corrected record verification

On 3 October 2026, full-record inspection verified that `W1581742186` links the original
PDF used by the explainer in its CiteSeerX location (same host and path, HTTP rather than
HTTPS), alongside the 2018 reprint DOI. Its title and author also match. The API reports
148 citations for this combined record. The initial omission above was overly strict:
the 2018 date alone did not establish that the record excluded the original. The page now
shows the verified count with its combined version scope. Always inspect record locations
as well as the headline publication date.
