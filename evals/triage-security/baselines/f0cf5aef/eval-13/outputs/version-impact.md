# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Summary by Stream

| Stream | Affected Versions | Not Affected Versions | Status |
|--------|-------------------|-----------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | -- | All versions affected; fix not present |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | Already fixed in 2.2.3+ |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

## Affects Versions Correction

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond
to any supported product version. No `2.0.x` stream exists in the Version Streams
configuration.

**Corrected Affects Versions** (for the 2.2.x scoped issue):
- Remove: RHTPA 2.0.0
- Add: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but are outside
this issue's scope. They are addressed via Case A cross-stream impact.

## Cross-Stream Impact (Case A)

This issue is scoped to stream **2.2.x**. Version impact analysis reveals that
stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9, which
is within the vulnerable range < 0.11.14).

Cross-stream impact comment to post on TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
> on lock file analysis. This stream is tracked by companion issues (see Related
> links) or may require separate PSIRT triage.

Since the 2.2.x stream is already fixed in its latest releases (2.2.3+), no
remediation tasks are needed for 2.2.x. The 2.1.x stream requires preemptive
remediation tasks (Case A).
