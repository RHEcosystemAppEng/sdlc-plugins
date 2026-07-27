# Step 0.3 -- Matrix Staleness Check

## Procedure

For each row in the Version Streams table from Security Configuration, read the
corresponding `security-matrix.md` file and extract the `Last-Updated` timestamp.
Compare it against the current date (2026-07-27) using the 14-day staleness threshold.

## Version Streams Checked

| Stream | Konflux Release Repo | Security Matrix Path |
|--------|----------------------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z/security-matrix.md |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z/security-matrix.md |

## Timestamp Extraction

Both streams share a single matrix file (mock fixture). The HTML comment at the
top of the file contains:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

Parsed timestamp: **2026-06-28T10:00:00Z**

## Staleness Calculation

- Current date: 2026-07-27
- Last-Updated: 2026-06-28
- Days elapsed: **29 days**
- Threshold: 14 days

## Result: STALE

The security matrix is **29 days old**, which exceeds the 14-day staleness threshold.

### Stream 2.1.x -- STALE

Security matrix for stream **2.1.x** was last updated on 2026-06-28 (29 days ago).
The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

### Stream 2.2.x -- STALE

Security matrix for stream **2.2.x** was last updated on 2026-06-28 (29 days ago).
The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

## Notes

- Both version streams share the same Last-Updated timestamp from the single
  matrix fixture file.
- The staleness warning should be presented to the engineer before proceeding
  with triage. The engineer must choose an option for each stream before
  Steps 1-8 can begin.
- A stale matrix can cause triage to miss newly released versions or use
  outdated source commit references.
