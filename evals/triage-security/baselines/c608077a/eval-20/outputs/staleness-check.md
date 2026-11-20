# Step 0.3 – Matrix Staleness Check — TC-8001

## Fixture evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (covers both configured streams) |
| `<!-- Last-Updated -->` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 14 days exactly (2026-07-12T10:00:00Z − 2026-06-28T10:00:00Z = 336 hours) |
| Staleness threshold | older than 14 days (default) |

## Per-stream result

| Stream | Konflux Release Repo | Last-Updated | Age | Stale? | Action |
|--------|----------------------|--------------|-----|--------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 days | No | Proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 days | No | Proceed |

## Result: FRESH — no warning

A matrix is stale only when it is **older than** 14 days. At 14 days exactly, it is
inside the threshold, so:

- No staleness warning is shown to the user.
- The Refresh now / Proceed anyway / Stop options are not offered, and triage does not
  wait for a user choice.
- A Last-Updated timestamp is present, so the missing-timestamp notice does not apply.
- The matrix file exists, so the Step 2.1 missing-file fallback does not apply.

Triage goes on to Step 1 (Data Extraction) using the current matrix.
