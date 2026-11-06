# Step 0.3 – Matrix Staleness Check (TC-8001)

## Mode

- Step 0.6: `FULLSEND_OUTPUT_DIR` absent → **interactive mode** (eval simulation; no external calls).
- Step 0 configuration validation: PASS — Repository Registry, Jira Configuration (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) all present in `claude-md-security-config.md`.

## Fixture evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (contains both stream matrices) |
| `<!-- Last-Updated -->` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | exactly 14 days (14d 0h 0m; 336 hours) |
| Staleness threshold | older than 14 days |
| Stale? | **No** — 14 days is not older than 14 days (boundary is inclusive of fresh) |

## Per-stream result

| Stream | Konflux Release Repo | Last-Updated | Age | Result |
|--------|----------------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 days | Fresh — proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 days | Fresh — proceed |

## Outcome

Matrix is within the 14-day threshold for all streams. **No staleness warning is
issued**, no Refresh/Proceed/Stop prompt is presented, and triage proceeds directly
to Step 0.5 / Step 1. (The age is recorded above only as fixture evidence.)
