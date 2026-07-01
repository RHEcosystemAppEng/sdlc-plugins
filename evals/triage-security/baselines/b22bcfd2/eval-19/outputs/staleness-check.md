# Step 0.3 -- Matrix Staleness Check

This step runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations have been attempted yet.

## Configuration Extracted (Step 0)

From the project CLAUDE.md Security Configuration:

| Field | Value |
|-------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column present) |

## Staleness Check

### Timestamp Extraction

The `security-matrix.md` file contains an HTML comment timestamp at the top of the file:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

- **Parsed timestamp**: 2026-05-01T10:00:00Z
- **Current date**: 2026-07-01
- **Age**: 61 days since last update
- **Threshold**: 14 days (default)
- **Result**: **STALE** -- the matrix is 61 days old, which exceeds the 14-day default threshold

### Streams Covered

The security matrix file covers both configured version streams:

| Stream | Last Updated | Age (days) | Status |
|--------|-------------|------------|--------|
| 2.1.x (rhtpa-release.0.3.z) | 2026-05-01 | 61 | STALE |
| 2.2.x (rhtpa-release.0.4.z) | 2026-05-01 | 61 | STALE |

Both streams share the same matrix file and therefore the same Last-Updated timestamp.

### Staleness Warning

> **Security matrix for stream 2.1.x was last updated on 2026-05-01 (61 days ago).** The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> **Security matrix for stream 2.2.x was last updated on 2026-05-01 (61 days ago).** The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

**Awaiting user choice before proceeding.** The triage is paused at Step 0.3 until the engineer selects an option for each stream.

## Execution Order Verification

The staleness check (Step 0.3) executes in the following position within the triage flow:

1. **Step 0** -- Validate Project Configuration (extract project key, Cloud ID, Security Config) -- COMPLETED
2. **Step 0.3** -- Matrix Staleness Check -- **CURRENT (paused, awaiting user input)**
3. Step 0.5 -- JIRA Access Initialization -- NOT YET REACHED
4. Step 1 -- Data Extraction -- NOT YET REACHED
5. Step 2+ -- Remaining triage steps -- NOT YET REACHED

No Jira operations (MCP calls, REST API calls, or JQL queries) have been attempted at this point. The staleness check runs before any Jira access is initialized, ensuring that the engineer can decide whether to refresh, proceed, or stop before any external system interaction occurs.

## Refresh Option Details

If the engineer selects **Refresh now**, the skill would:

1. Invoke the matrix population logic from setup Step 10.6 for the selected stream
2. Query the Konflux release repo's git history (tags, release branches) to discover released versions
3. For each version, extract image digest, build date, and source commits per repository from the repo's build metadata
4. Identify retags (versions with identical source commits)
5. Write the discovered rows into the local `security-matrix.md` file with an updated `Last-Updated` timestamp
6. Present the populated matrix to the user for confirmation before writing
7. After population completes, continue triage with the refreshed matrix

If the engineer selects **Proceed anyway**, triage continues with the current (stale) matrix data. The version impact analysis in Step 2 will use the existing supportability matrix rows, which may not include versions released after 2026-05-01.

If the engineer selects **Stop**, triage halts immediately. The engineer can investigate whether new versions have been released since the last matrix update and manually refresh the matrix before re-running triage.
