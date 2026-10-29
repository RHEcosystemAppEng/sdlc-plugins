# Step 0.3 -- Matrix Staleness Check

## Extraction Evidence

- **Source HTML comment**: `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`
- **Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`
- **Comparison clock (evaluation clock)**: `2026-07-12T10:00:00Z`

## Fixture Evidence

- **Evaluation clock**: `2026-07-12T10:00:00Z`
- **Matrix Last-Updated**: `2026-05-01T10:00:00Z`
- **Computed matrix age**: 72 days
- **Staleness threshold**: 14 days
- **Stale**: Yes (72 days > 14 days)

## Staleness Detection Output

The security matrix file covers both configured version streams (2.1.x and 2.2.x) and contains a single `Last-Updated` timestamp. The matrix age of 72 days exceeds the 14-day staleness threshold.

### Stream: 2.1.x (rhtpa-release.0.3.z)

Security matrix for stream **2.1.x** was last updated on 2026-05-01 (72 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x (rhtpa-release.0.4.z)

Security matrix for stream **2.2.x** was last updated on 2026-05-01 (72 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

---

Awaiting user choice for each stream before proceeding with triage.
