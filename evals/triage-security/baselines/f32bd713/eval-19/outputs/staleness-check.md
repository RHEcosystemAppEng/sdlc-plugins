# Step 0.3 -- Matrix Staleness Check

## Extraction Evidence

- **Source Last-Updated HTML comment**: `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`
- **Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`
- **Comparison clock (evaluation clock)**: `2026-07-12T10:00:00Z`

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z
- **Matrix Last-Updated**: 2026-05-01T10:00:00Z
- **Computed matrix age**: 72 days (May 1 to July 12: 30 days remaining in May + 30 days in June + 12 days in July = 72 days)
- **Staleness threshold**: 14 days
- **Result**: STALE (72 days > 14-day threshold)

## Staleness Warning

### Stream 2.1.x

Security matrix for stream **2.1.x** was last updated on 2026-05-01
(72 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

### Stream 2.2.x

Security matrix for stream **2.2.x** was last updated on 2026-05-01
(72 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate
