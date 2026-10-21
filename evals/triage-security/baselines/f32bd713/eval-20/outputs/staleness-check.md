# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock (fixed UTC scenario time):** 2026-07-12T10:00:00Z
- **Matrix `Last-Updated` timestamp:** 2026-06-28T10:00:00Z
- **Computed matrix age:** 14 days (exactly)
- **Staleness threshold:** older than 14 days

## Version Streams Checked

The Security Configuration defines two version streams, both served by a single
`security-matrix.md` file:

| Stream | Konflux Release Repo | Security Matrix Path |
|--------|----------------------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | (local) |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | (local) |

## Staleness Result

**PASS -- matrix is within the freshness threshold.**

The `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) is exactly 14 days before
the evaluation clock (`2026-07-12T10:00:00Z`). The staleness rule triggers when
the matrix is **older than** 14 days. At exactly 14 days the matrix is at the
boundary but not beyond it, so it is considered fresh.

No user warning is required. Triage proceeds with the current matrix data.
