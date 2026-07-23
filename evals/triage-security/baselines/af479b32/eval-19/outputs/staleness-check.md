# Step 0.3 -- Matrix Staleness Check

## Issue: TC-8001 (CVE-2026-31812)

### Configuration

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Staleness Detection Results

**Current date**: 2026-07-23
**Staleness threshold**: 14 days

---

#### Stream 2.1.x (rhtpa-release.0.3.z)

- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Age**: 83 days
- **Status**: STALE

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (83 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

#### Stream 2.2.x (rhtpa-release.0.4.z)

- **Last-Updated timestamp**: 2026-05-01T10:00:00Z
- **Age**: 83 days
- **Status**: STALE

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (83 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

### Summary

Both version streams have stale security matrices (83 days old, threshold is 14 days). User action is required before proceeding with triage. The matrices were last updated on 2026-05-01 and may not reflect releases published since then.
