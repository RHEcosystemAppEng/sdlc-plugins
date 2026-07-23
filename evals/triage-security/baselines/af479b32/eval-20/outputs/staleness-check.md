# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams checked**: 2.1.x, 2.2.x
- **Matrix source file**: security-matrix-mock.md (single file covering both streams)
- **Staleness threshold**: 14 days

## Timestamp Extraction

The `security-matrix-mock.md` file contains the following HTML comment at the top:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

**Parsed timestamp**: 2026-06-28T10:00:00Z

## Staleness Calculation

- **Last-Updated**: 2026-06-28
- **Current date**: 2026-07-23
- **Age**: 25 days
- **Threshold**: 14 days
- **Result**: STALE (25 days > 14-day threshold)

## Staleness Warning

Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (25 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for these streams
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

## Disposition

Per the eval instructions, no external tool calls are permitted. In a live triage, the engineer would be prompted to choose one of the three options above before proceeding. For this eval, we document the staleness finding and proceed with the current matrix data (equivalent to option 2).

## Stream-by-Stream Detail

### Stream 2.1.x (rhtpa-release.0.3.z)

| Field | Value |
|-------|-------|
| Konflux Release Repo | git.example.com/rhtpa/rhtpa-release.0.3.z |
| Local Path | /home/dev/repos/rhtpa-release.0.3.z |
| Matrix Last-Updated | 2026-06-28T10:00:00Z |
| Days since update | 25 |
| Staleness status | STALE |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Field | Value |
|-------|-------|
| Konflux Release Repo | git.example.com/rhtpa/rhtpa-release.0.4.z |
| Local Path | /home/dev/repos/rhtpa-release.0.4.z |
| Matrix Last-Updated | 2026-06-28T10:00:00Z |
| Days since update | 25 |
| Staleness status | STALE |
