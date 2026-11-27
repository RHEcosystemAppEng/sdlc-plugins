# Step 0.3 – Matrix Staleness Check (TC-8001)

## Fixture evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for this check) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (covers both streams) |
| `Last-Updated` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 14 days 0 hours (exactly 14 days, 336 hours) |
| Staleness threshold | older than 14 days |
| Stale? | **No** (14 days is not older than 14 days) |

## Per-stream result

| Stream | Konflux Release Repo | Last-Updated | Age | Result |
|--------|----------------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 days | Fresh, proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 days | Fresh, proceed |

## Outcome

The timestamp is present and parses correctly, and the matrix is within the 14-day
threshold for both streams. The staleness warning does not apply, so the
Refresh / Proceed / Stop prompt was **not** shown. Triage goes straight on to Step 0.5
and Step 1 with no need for user input.
