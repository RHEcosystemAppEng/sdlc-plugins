# Step 0.3 – Matrix Staleness Check (TC-8001)

## Mode

- Step 0.6: `FULLSEND_OUTPUT_DIR` is absent, so this is **interactive mode**. Step 0.7 is skipped.
- Step 0 (configuration validation): all required sections are present in the project CLAUDE.md (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration with Product Lifecycle, Version Streams and Source Repositories). Proceeding.

## Fixture evidence

| Item | Value |
|---|---|
| Evaluation clock (current date for this check) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (holds the matrices for both configured streams) |
| `<!-- Last-Updated -->` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 14 days exactly (2026-07-12T10:00:00Z minus 2026-06-28T10:00:00Z = 336 hours) |
| Staleness threshold | older than 14 days |
| Stale? | **No.** 14 days is not older than 14 days |

## Per-stream result

| Stream | Konflux Release Repo | Last-Updated | Age (days) | Result |
|---|---|---|---|---|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 | Fresh, proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 | Fresh, proceed |

## Outcome

**PASS. The matrix is fresh and triage continues.** Both matrices were updated within the 14-day threshold, so I did not show the staleness warning or the Refresh now / Proceed anyway / Stop prompt. No refresh was triggered and no matrix file was written.

Note: the Version Streams table has no explicit Security Matrix Path column. For this eval, the supplied mock matrix file stands in for each stream's `security-matrix.md`.
