# Step 0.3 -- Matrix Staleness Check

Step 0.3 runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations
are attempted before the staleness check completes.

## Configuration

Extracted from Security Configuration in CLAUDE.md:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Default staleness threshold: **14 days**

## Staleness Check Results

### Stream 2.1.x (rhtpa-release.0.3.z)

**Read matrix file** at `/home/dev/repos/rhtpa-release.0.3.z/security-matrix.md`.

**Extracted timestamp** from HTML comment:
```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```
Parsed ISO 8601 value: **2026-05-01T10:00:00Z**

**Staleness evaluation:**
- Last updated: 2026-05-01
- Current date: 2026-08-24
- Age: **115 days**
- Threshold: 14 days
- Result: **STALE** (115 days > 14 days)

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (115 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

### Stream 2.2.x (rhtpa-release.0.4.z)

**Read matrix file** at `/home/dev/repos/rhtpa-release.0.4.z/security-matrix.md`.

**Extracted timestamp** from HTML comment:
```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```
Parsed ISO 8601 value: **2026-05-01T10:00:00Z**

**Staleness evaluation:**
- Last updated: 2026-05-01
- Current date: 2026-08-24
- Age: **115 days**
- Threshold: 14 days
- Result: **STALE** (115 days > 14 days)

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (115 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Summary

Both version streams have stale security matrices (115 days old, threshold is 14 days).
Triage is **blocked** pending the user's decision for each stream. No Jira access
(Step 0.5) or subsequent triage steps will execute until the staleness check is resolved.
