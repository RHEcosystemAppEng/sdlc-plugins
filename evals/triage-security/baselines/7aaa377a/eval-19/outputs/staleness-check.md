# Step 0.3 -- Matrix Staleness Check

This step runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations
have been attempted at this point -- the staleness check is performed immediately
after Step 0 configuration validation.

## Procedure

For each row in the Version Streams table, read the security matrix file and extract
the `<!-- Last-Updated: <ISO-8601> -->` HTML comment to determine when the matrix
was last refreshed.

## Stream: 2.1.x

**Matrix file**: security-matrix.md (covering rhtpa-release.0.3.z)

**Timestamp extraction**: Read the HTML comment at the top of the matrix file:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed value**: 2026-05-01T10:00:00Z (ISO 8601)

**Staleness calculation**:
- Last updated: 2026-05-01
- Current date: 2026-07-28
- Days since last update: **88 days**
- Default threshold: 14 days
- Result: **STALE** (88 days > 14-day threshold)

### Warning

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (88 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Stream: 2.2.x

**Matrix file**: security-matrix.md (covering rhtpa-release.0.4.z)

**Timestamp extraction**: Read the HTML comment at the top of the matrix file:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed value**: 2026-05-01T10:00:00Z (ISO 8601)

**Staleness calculation**:
- Last updated: 2026-05-01
- Current date: 2026-07-28
- Days since last update: **88 days**
- Default threshold: 14 days
- Result: **STALE** (88 days > 14-day threshold)

### Warning

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (88 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Summary

Both version streams (2.1.x and 2.2.x) share the same Last-Updated timestamp
(2026-05-01T10:00:00Z), which is 88 days old -- well beyond the 14-day default
staleness threshold. The matrix data may not reflect versions released after
2026-05-01.

**No Jira operations have been performed.** Step 0.3 completes (or blocks on user
input) before Step 0.5 (JIRA Access Initialization) begins. The triage cannot
proceed past this point until the user selects an option for each stale stream.

### Option details

| Option | Action |
|--------|--------|
| **1. Refresh now** | Re-run setup Step 10.6 to query the Konflux release repo for the latest versions, rebuild the supportability matrix, and write an updated `Last-Updated` timestamp. Triage resumes with fresh data. |
| **2. Proceed anyway** | Accept the risk that the matrix may be missing recently released versions or using outdated source commit references. Triage continues with the current matrix as-is. |
| **3. Stop** | Halt triage entirely. The user can investigate why the matrix is stale, manually update it, or re-run `/setup` before retrying triage. |
