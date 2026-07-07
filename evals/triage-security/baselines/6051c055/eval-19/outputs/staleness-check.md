# Step 0.3 -- Matrix Staleness Check

## Issue: TC-8001 (CVE-2026-31812 quinn-proto)

Before proceeding with triage, verifying that each version stream's security matrix
has been updated recently enough to reflect the current release landscape.

---

### Stream: 2.1.x

**Matrix file**: security-matrix.md (rhtpa-release.0.3.z)
**Last-Updated timestamp**: 2026-05-01T10:00:00Z
**Current date**: 2026-07-07
**Days since update**: 67 days
**Staleness threshold**: 14 days
**Result**: STALE

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (67 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

### Stream: 2.2.x

**Matrix file**: security-matrix.md (rhtpa-release.0.4.z)
**Last-Updated timestamp**: 2026-05-01T10:00:00Z
**Current date**: 2026-07-07
**Days since update**: 67 days
**Staleness threshold**: 14 days
**Result**: STALE

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (67 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

---

**Action required**: Awaiting user choice for each stale stream before proceeding
to Step 0.5 (JIRA Access Initialization). No Jira operations have been performed.
