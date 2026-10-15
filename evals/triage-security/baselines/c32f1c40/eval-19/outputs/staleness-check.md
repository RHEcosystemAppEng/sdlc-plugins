# Step 0.3 -- Matrix Staleness Check

This step runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations have been attempted at this point.

## Extraction Evidence

**Source HTML comment** (from security-matrix-stale-mock.md, line 1):

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`

**Comparison clock (evaluation clock)**: `2026-07-12T10:00:00Z`

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z (fixed UTC scenario time)
- **Matrix Last-Updated**: 2026-05-01T10:00:00Z
- **Computed matrix age**: 72 days (2026-05-01 to 2026-07-12)
- **Staleness threshold**: 14 days (default)
- **Stale?**: YES -- 72 days exceeds the 14-day threshold by 58 days

## Staleness Detection

For each row in the Version Streams table in Security Configuration, the matrix file was read and its `Last-Updated` HTML comment was extracted and parsed.

### Stream: 2.1.x (rhtpa-release.0.3.z)

The security matrix file for stream 2.1.x was read. The `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` HTML comment was found and parsed.

Matrix age: 72 days (last updated 2026-05-01T10:00:00Z, current date 2026-07-12T10:00:00Z).

72 days > 14-day threshold -- **STALE**.

### Stream: 2.2.x (rhtpa-release.0.4.z)

The security matrix file for stream 2.2.x was read. The `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` HTML comment was found and parsed.

Matrix age: 72 days (last updated 2026-05-01T10:00:00Z, current date 2026-07-12T10:00:00Z).

72 days > 14-day threshold -- **STALE**.

## Staleness Warning

> Security matrix for stream **2.1.x** was last updated on 2026-05-01 (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01 (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding to Step 0.5 (JIRA Access Initialization) and subsequent triage steps. No Jira operations or version impact analysis will be performed until the user confirms how to handle the stale matrix.
