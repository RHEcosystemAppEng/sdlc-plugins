# Step 0.3 -- Matrix Staleness Check

## Timestamp Extraction

Read the `security-matrix.md` file at the configured Security Matrix Path for each version stream.

**HTML comment found at the top of the file:**
```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed timestamp**: 2026-05-01T10:00:00Z (ISO 8601 format)

## Staleness Evaluation

- **Current date**: 2026-07-09
- **Last updated**: 2026-05-01
- **Days since last update**: 69 days
- **Threshold**: 14 days (default)
- **Result**: **STALE** -- the matrix is 69 days old, which exceeds the 14-day threshold

## Staleness Warning

The following warning is presented to the engineer:

---

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (69 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (69 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

**Waiting for the user's choice before proceeding.**

## Step Ordering

Step 0.3 (Matrix Staleness Check) runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations are attempted before the staleness check completes. If the user chooses "Stop", triage halts without having made any Jira API calls.

## Options Explained

1. **Refresh now**: Invokes the matrix population logic from setup Step 10.6 for the selected stream. After population completes (which writes an updated `Last-Updated` timestamp), triage continues with the refreshed matrix.
2. **Proceed anyway**: The engineer acknowledges the staleness risk and continues triage with the current (potentially outdated) matrix data.
3. **Stop**: Halt triage entirely so the engineer can investigate why the matrix has not been updated in 69 days. No further steps are executed.
