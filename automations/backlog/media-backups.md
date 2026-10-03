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
