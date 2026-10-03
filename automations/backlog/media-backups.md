# Pending media backups

Backups here are deferred work, not a blocker for generation or authorized publication.
Keep local exports and narration until they have been archived. Each row represents the
latest files for one paper/export kind; reruns update the row rather than duplicate it.

When Expansion is available, run `uv run --frozen paper-video backup-pending`.
The command verifies each snapshot and removes only successful rows. Remaining failures
stay listed with their latest reason. See [the backup guide](../../docs/media-backup-plan.md).

The pipeline maintains this table. Do not remove a row before its backup verifies.

| Paper | Export | Last deferred at | Reason |
| --- | --- | --- | --- |
| frontier-models-are-capable-of-in-context-scheming | full | 2026-10-02T21:12:27.579879-04:00 | backup volume is not mounted: /Volumes/Expansion; local video is retained |
| frontier-models-are-capable-of-in-context-scheming | short | 2026-10-02T21:12:27.580431-04:00 | backup volume is not mounted: /Volumes/Expansion; local video is retained |
| stress-testing-deliberative-alignment-for-anti-scheming-training | full | 2026-10-02T21:12:59.603252-04:00 | backup volume is not mounted: /Volumes/Expansion; local video is retained |
| stress-testing-deliberative-alignment-for-anti-scheming-training | short | 2026-10-02T21:16:27.725546-04:00 | backup volume is not mounted: /Volumes/Expansion; local video is retained |
