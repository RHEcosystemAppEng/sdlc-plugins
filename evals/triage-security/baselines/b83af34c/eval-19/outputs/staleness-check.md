# Step 0.3 -- Matrix Staleness Check

## Execution Context

This step runs **before** Step 0.5 (JIRA Access Initialization). No Jira MCP calls,
REST API calls, or any Jira operations have been attempted at this point. The staleness
check is a pre-flight validation that gates whether triage should proceed with the
current matrix data.

## Timestamp Extraction

Reading the security matrix file for all configured Version Streams.

**Source file**: `security-matrix-stale-mock.md` (used as `security-matrix.md` for both streams)

**Extracted HTML comment**:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`
**Current date**: `2026-07-31`
**Days since last update**: 90 days
**Staleness threshold**: 14 days (default)
**Result**: **STALE** (90 days > 14 days)

## Staleness Warnings

### Stream: 2.1.x

Security matrix for stream **2.1.x** was last updated on 2026-05-01
(90 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x

Security matrix for stream **2.2.x** was last updated on 2026-05-01
(90 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

## Step Ordering Confirmation

| Step | Name | Status |
|------|------|--------|
| 0 | Validate Project Configuration | Completed |
| 0.3 | Matrix Staleness Check | **Completed (this step) -- staleness detected, awaiting user choice** |
| 0.5 | JIRA Access Initialization | NOT YET STARTED -- blocked until Step 0.3 resolves |
| 0.7 | Assign and Transition | NOT YET STARTED -- blocked until Step 0.5 completes |
| 1+ | Data Extraction and beyond | NOT YET STARTED |

No Jira operations have been attempted. The skill is waiting for the user to choose
one of the three options for each stale stream before proceeding to Step 0.5
(JIRA Access Initialization).
