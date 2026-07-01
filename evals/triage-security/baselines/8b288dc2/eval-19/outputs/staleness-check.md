# Step 0.3 — Matrix Staleness Check

## Configuration

- **Current date**: 2026-07-01
- **Staleness threshold**: 14 days
- **Version Streams checked**: 2

## Stream: 2.1.x

- **Security Matrix Path**: security-matrix.md (rhtpa-release.0.3.z)
- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Days since update**: 61 days

> **Warning:** Security matrix for stream **2.1.x** was last updated on 2026-05-01 (61 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

## Stream: 2.2.x

- **Security Matrix Path**: security-matrix.md (rhtpa-release.0.4.z)
- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Days since update**: 61 days

> **Warning:** Security matrix for stream **2.2.x** was last updated on 2026-05-01 (61 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

---

**Note**: Step 0.3 runs BEFORE Step 0.5 (Jira Access Initialization). No Jira operations have been performed at this point. The staleness check uses only local file timestamps from the `security-matrix.md` files configured in the Version Streams table. User must select an option for each stale stream before triage proceeds.
