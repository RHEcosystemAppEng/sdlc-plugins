# Step 0.3 – Matrix Staleness Check — TC-8001

## Fixture Evidence

| Item | Value |
|------|-------|
| Execution mode | Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` absent) |
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Staleness threshold | 14 days (default) — warn only if matrix is **older than** 14 days |
| Matrix source | `security-matrix-mock.md` (covers both configured streams) |
| `<!-- Last-Updated -->` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 2026-07-12T10:00:00Z − 2026-06-28T10:00:00Z = **14 days, 0 hours** (exactly 336 hours) |

## Per-Stream Results

| Stream | Konflux Release Repo | Last-Updated | Age | Older than 14 days? | Result |
|--------|----------------------|--------------|-----|---------------------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 days | No (14 is not > 14) | FRESH — pass |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 days | No (14 is not > 14) | FRESH — pass |

## Outcome

- Timestamp found and parsed for every stream (no "missing timestamp" advisory needed).
- Matrix file exists for every stream (Step 2.1 fallback not triggered).
- The matrix age is exactly at the 14-day threshold, which is **within** the threshold —
  the staleness condition is "older than 14 days", so it is not met.
- **No staleness warning is issued and no Refresh / Proceed / Stop prompt is presented.**
  Triage proceeds directly with the current matrix.

The evaluation clock and computed age above are recorded only as fixture evidence;
they do not constitute a user-facing warning.
