# Step 0.3 -- Matrix Staleness Check

## Execution Context

Step 0.3 runs **before** Step 0.5 (JIRA Access Initialization). No Jira API calls or MCP operations have been attempted at this point. The staleness check is a local-only operation that reads the `security-matrix.md` file timestamps to verify recency before any triage work begins.

## Timestamp Extraction

Read the `security-matrix.md` file for each configured Version Stream. The file contains an HTML comment at the top with the Last-Updated timestamp:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

Parsed ISO 8601 value: **2026-05-01T10:00:00Z**

## Staleness Evaluation

- **Current date**: 2026-07-01
- **Last-Updated**: 2026-05-01 (parsed from HTML comment `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`)
- **Age**: 61 days
- **Threshold**: 14 days (default)
- **Result**: **STALE** -- the matrix is 61 days old, exceeding the 14-day threshold by 47 days

## Staleness Warning -- Stream 2.1.x

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (61 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

## Staleness Warning -- Stream 2.2.x

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (61 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

## Step Sequencing

| Step | Name | Status |
|------|------|--------|
| 0 | Validate Configuration | Completed -- Security Configuration present and valid |
| 0.3 | Matrix Staleness Check | **Blocked -- awaiting user response to staleness warning** |
| 0.5 | JIRA Access Initialization | Not started -- waiting for Step 0.3 to complete |
| 1 | Data Extraction | Not started |
| 1.5 | External CVE Data Enrichment | Not started |
| 2 | Version Impact Analysis | Not started |

No Jira operations (MCP calls, REST API calls, JQL searches, issue fetches) have been attempted. Step 0.3 gates all subsequent steps -- the triage will not proceed to Step 0.5 (JIRA Access Initialization) or any later step until the engineer responds to the staleness warning with one of the three options.

## User Response Handling

If the user chooses:

1. **Refresh now**: Invoke matrix population logic from setup Step 10.6 for the selected stream(s). After population completes (which writes an updated `Last-Updated` timestamp to the security-matrix.md file), continue with the refreshed matrix data.

2. **Proceed anyway**: Accept the stale matrix data and continue to Step 0.5 (JIRA Access Initialization), then proceed with the full triage flow using the existing matrix. The version impact analysis in Step 2 will use the current matrix data, which may not include recently released versions.

3. **Stop**: Halt triage execution immediately. The engineer can investigate whether new versions have been released since 2026-05-01 and manually update the matrix or run `/setup` before re-invoking the triage skill.
