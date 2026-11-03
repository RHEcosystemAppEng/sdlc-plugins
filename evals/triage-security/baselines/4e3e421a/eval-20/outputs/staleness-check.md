# Step 0.3 – Matrix Staleness Check (TC-8001)

## Execution context

- Mode (Step 0.6): **interactive** (`FULLSEND_OUTPUT_DIR` absent)
- Step 0 configuration: valid. Repository Registry, Jira Configuration (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present.
- Matrix source: `security-matrix-mock.md` (eval fixture standing in for each stream's local `security-matrix.md`)
- Staleness threshold: 14 days (default). A matrix is stale only if it is **older than** 14 days.

## Fixture evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Matrix `Last-Updated` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 14 days 0 hours (exactly 336 hours) |
| Threshold | older than 14 days |
| Result | **Not stale**: 14 days is not more than 14 days |

## Per-stream result

| Stream | Konflux Release Repo | Last-Updated | Age | Status |
|--------|----------------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 days | Fresh, within threshold |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 days | Fresh, within threshold |

## Outcome

Both version stream matrices are within the 14-day threshold. **No staleness warning is shown.** The Refresh / Proceed / Stop prompt is not presented, and no matrix refresh or write takes place. Triage goes on to Step 0.5 / 0.8 / Step 1 without blocking.

The evaluation clock and the computed age above are recorded only as fixture evidence. They are not a user-facing warning.
