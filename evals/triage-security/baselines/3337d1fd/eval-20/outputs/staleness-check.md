# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Current date**: 2026-07-22
- **Staleness threshold**: 14 days
- **Version Streams checked**: 2 streams from Security Configuration

## Stream Results

### Stream 2.1.x (rhtpa-release.0.3.z)

- **Matrix file**: security-matrix-mock.md (covers both streams in this eval setup)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 24 days (from 2026-06-28 to 2026-07-22)
- **Status**: STALE -- exceeds the 14-day threshold by 10 days

### Stream 2.2.x (rhtpa-release.0.4.z)

- **Matrix file**: security-matrix-mock.md (same file as above)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 24 days (from 2026-06-28 to 2026-07-22)
- **Status**: STALE -- exceeds the 14-day threshold by 10 days

## Staleness Warning

Both version streams share a single matrix file with a Last-Updated timestamp of 2026-06-28, which is 24 days old. This exceeds the 14-day staleness threshold.

Per the skill protocol, the following warning would be presented to the engineer for each stream:

> Security matrix for stream **2.1.x** was last updated on 2026-06-28
> (24 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-06-28
> (24 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Outcome

The engineer must choose an option before triage can proceed to Step 1. If the engineer selects "Proceed anyway" for both streams, triage continues with the current (potentially outdated) matrix data. If "Refresh now" is selected, setup Step 10.6 is invoked to repopulate the matrix and update the Last-Updated timestamp before continuing.

## Methodology

1. Read the `<!-- Last-Updated: <ISO-8601> -->` HTML comment from the top of each stream's security-matrix.md file
2. Parsed the ISO 8601 timestamp: `2026-06-28T10:00:00Z`
3. Computed the difference between the current date (2026-07-22) and the timestamp date (2026-06-28): 24 days
4. Compared against the 14-day default threshold: 24 > 14, therefore stale
