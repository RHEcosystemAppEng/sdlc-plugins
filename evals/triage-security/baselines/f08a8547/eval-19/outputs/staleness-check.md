# Step 0.3 -- Matrix Staleness Check

## Procedure

Step 0.3 runs **before** Step 0.5 (JIRA Access Initialization). No Jira
operations are attempted before the staleness check completes.

For each row in the Version Streams table from Security Configuration, the
`security-matrix.md` file is read and its `<!-- Last-Updated: ... -->` HTML
comment timestamp is extracted and compared against the current date.

## Timestamp Extraction

The security matrix file contains the following HTML comment at the top:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

Parsed ISO 8601 value: **2026-05-01T10:00:00Z**

## Staleness Evaluation

| Stream | Matrix Path | Last-Updated | Days Since Update | Threshold | Status |
|--------|-------------|--------------|-------------------|-----------|--------|
| 2.1.x | /home/dev/repos/rhtpa-release.0.3.z/security-matrix.md | 2026-05-01 | 130 days | 14 days | **STALE** |
| 2.2.x | /home/dev/repos/rhtpa-release.0.4.z/security-matrix.md | 2026-05-01 | 130 days | 14 days | **STALE** |

Both streams are sourced from the same matrix file, which has a single
Last-Updated timestamp of 2026-05-01T10:00:00Z. The current date is
2026-09-08, making the matrix **130 days old** -- far exceeding the
14-day default staleness threshold.

## Staleness Warning

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (130 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (130 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding to Step 0.5 (JIRA Access Initialization).
