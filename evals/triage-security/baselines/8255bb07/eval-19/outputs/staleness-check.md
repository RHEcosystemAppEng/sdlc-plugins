# Step 0.3 — Matrix Staleness Check

## Issue: TC-8001

## Staleness Detection

For each configured Version Stream, the `security-matrix.md` file was checked
for a `<!-- Last-Updated: ... -->` timestamp and compared against the current
date (2026-07-06) using the 14-day staleness threshold.

### Stream: 2.1.x (rhtpa-release.0.3.z)

- **Security Matrix Path**: /home/dev/repos/rhtpa-release.0.3.z/security-matrix.md
- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Days since update**: 66 days
- **Threshold**: 14 days
- **Result**: STALE

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (66 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Awaiting user choice before proceeding.

### Stream: 2.2.x (rhtpa-release.0.4.z)

- **Security Matrix Path**: /home/dev/repos/rhtpa-release.0.4.z/security-matrix.md
- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Days since update**: 66 days
- **Threshold**: 14 days
- **Result**: STALE

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (66 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Awaiting user choice before proceeding.

## Step Ordering Note

Step 0.3 (Matrix Staleness Check) runs BEFORE Step 0.5 (JIRA Access
Initialization). No Jira API calls have been made at this point. The
staleness check is a local-only operation that reads timestamps from
on-disk `security-matrix.md` files to gate further triage progression.
