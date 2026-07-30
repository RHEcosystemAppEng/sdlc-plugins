# Step 0.3 -- Matrix Staleness Check

## Configuration Validated (Step 0)

The following configuration was extracted from the project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | _(not configured)_ |
| PS Component field | _(not configured)_ |
| Stream custom field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream _(default -- no Deployment Context column)_ |

---

## Staleness Check Results

**Current date**: 2026-07-30

The security matrix file covers both streams (2.1.x and 2.2.x) in a single document.

### Stream: 2.1.x (rhtpa-release.0.3.z)

- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 32 days
- **Threshold**: 14 days
- **Result**: **STALE** -- matrix exceeds the 14-day threshold

> Security matrix for stream **2.1.x** was last updated on 2026-06-28
> (32 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x (rhtpa-release.0.4.z)

- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 32 days
- **Threshold**: 14 days
- **Result**: **STALE** -- matrix exceeds the 14-day threshold

> Security matrix for stream **2.2.x** was last updated on 2026-06-28
> (32 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

## Conclusion

Both version streams have a `Last-Updated` timestamp of 2026-06-28, which is 32 days ago. This exceeds the 14-day staleness threshold. A staleness warning is displayed for both streams with options to refresh, proceed anyway, or stop. The engineer must choose before triage can continue to Step 0.5 (JIRA Access Initialization).
