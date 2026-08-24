# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams checked**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Staleness threshold**: 14 days
- **Current date**: 2026-08-24

## Matrix File

Both streams share a single matrix file: `security-matrix-mock.md`

### Timestamp Extraction

The file contains an HTML comment timestamp at line 1:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

- **Parsed timestamp**: 2026-06-28T10:00:00Z
- **Age**: 57 days (from 2026-06-28 to 2026-08-24)

## Staleness Evaluation

| Stream | Matrix File | Last-Updated | Age (days) | Threshold (days) | Result |
|--------|-------------|--------------|------------|-------------------|--------|
| 2.1.x  | security-matrix-mock.md | 2026-06-28 | 57 | 14 | STALE |
| 2.2.x  | security-matrix-mock.md | 2026-06-28 | 57 | 14 | STALE |

## Result: STALE

The security matrix was last updated on 2026-06-28 (57 days ago), which exceeds the 14-day staleness threshold. Under normal operation, the following warning would be presented to the engineer:

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (57 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for these streams
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Eval Note

For the purposes of this eval, we proceed with the current matrix data as provided in the mock file. No external tools are called to refresh the matrix.
