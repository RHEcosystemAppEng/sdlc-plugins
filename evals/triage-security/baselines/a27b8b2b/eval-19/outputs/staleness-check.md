# Step 0.3 -- Matrix Staleness Check

This step executes **before** Step 0.5 (JIRA Access Initialization). No Jira
operations have been attempted at this point -- the staleness check is the first
validation after Step 0 configuration extraction.

## Configuration Extracted (Step 0)

From the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Check Procedure

For each row in the Version Streams table, read the corresponding
`security-matrix.md` file and extract the `Last-Updated` timestamp from
the HTML comment at the top of the file.

### Reading the timestamp

The security-matrix.md file begins with:

```html
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

**Parsed ISO 8601 value**: `2026-05-01T10:00:00Z`
**Current date**: `2026-07-27`
**Days since last update**: **87 days**
**Default staleness threshold**: **14 days**

### Staleness evaluation

Both streams (2.1.x and 2.2.x) are covered by the same security-matrix.md
file, which shares a single `Last-Updated` timestamp. Since 87 days exceeds
the 14-day default threshold, the matrix is **stale** for both streams.

---

## Stream: 2.1.x -- STALE

> **Warning**: Security matrix for stream **2.1.x** was last updated on **2026-05-01**
> (**87 days ago**). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Stream: 2.2.x -- STALE

> **Warning**: Security matrix for stream **2.2.x** was last updated on **2026-05-01**
> (**87 days ago**). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Summary

| Stream | Last Updated | Days Since Update | Threshold | Status |
|--------|-------------|-------------------|-----------|--------|
| 2.1.x | 2026-05-01 | 87 days | 14 days | STALE |
| 2.2.x | 2026-05-01 | 87 days | 14 days | STALE |

**Action required**: The user must choose one of the three options for each
stale stream before triage can proceed to Step 0.5 (JIRA Access Initialization)
and subsequent steps. No Jira mutations or `git show` operations are performed
until the staleness check is resolved.

### Option behavior

- **Refresh now (Option 1)**: Invokes setup Step 10.6 to re-populate the
  supportability matrix for the selected stream from the Konflux release repo.
  This will query the repo's git history (tags, release branches) to discover
  released versions, extract build metadata, and write an updated
  `security-matrix.md` with a fresh `Last-Updated` timestamp. After population
  completes, triage continues with the refreshed matrix.

- **Proceed anyway (Option 2)**: Continue triage with the current (stale)
  matrix data. The version impact analysis in Step 2 will use the existing
  supportability matrix rows, which may be missing recently released versions
  or may reference outdated source commit tags.

- **Stop (Option 3)**: Halt triage execution entirely. The user can investigate
  why the matrix is stale (e.g., missing releases, configuration drift) and
  re-run triage after resolving the issue.
