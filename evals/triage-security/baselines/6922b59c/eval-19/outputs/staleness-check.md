# Step 0.3 -- Matrix Staleness Check

## Extraction Evidence

- **Source Last-Updated HTML comment**: `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`
- **Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`
- **Comparison clock (evaluation clock)**: `2026-07-12T10:00:00Z`

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z
- **Matrix Last-Updated**: 2026-05-01T10:00:00Z
- **Computed matrix age**: 72 days
- **Staleness threshold**: 14 days
- **Staleness detected**: Yes (72 days > 14 days)

## Staleness Warning

The security matrix file contains a single `Last-Updated` timestamp covering both configured version streams (2.1.x and 2.2.x). The timestamp is 72 days old relative to the evaluation clock, which exceeds the 14-day staleness threshold.

### Stream: 2.1.x (rhtpa-release.0.3.z)

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x (rhtpa-release.0.4.z)

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Resolution

Awaiting user choice before proceeding with triage. The stale matrix may not reflect releases published after 2026-05-01, which could cause triage to miss newly released versions or use outdated source commit references.
