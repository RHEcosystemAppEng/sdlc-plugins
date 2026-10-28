# Step 2 -- Version Impact Analysis for CVE-2026-31812

CVE-2026-31812: quinn-proto -- affected range: versions before 0.11.14, fixed version: 0.11.14

## Combined Version Impact Table

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | fix introduced here |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

## Stream-by-Stream Summary

### Stream 2.1.x (rhtpa-release.0.3.z)

- **Affected versions**: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
- **Not affected versions**: (none)
- **Upstream fix status**: NOT fixed on release/0.3.z (latest tag v0.3.12 ships quinn-proto 0.11.9)
- **Remediation needed**: YES -- upstream backport required to bump quinn-proto to >= 0.11.14

### Stream 2.2.x (rhtpa-release.0.4.z)

- **Affected versions**: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12)
- **Not affected versions**: 2.2.3 (quinn-proto 0.11.14), 2.2.4 (quinn-proto 0.11.14)
- **Upstream fix status**: FIXED on release/0.4.z (latest tag v0.4.12 ships quinn-proto 0.11.14)
- **Remediation needed**: NO -- fix already incorporated in versions 2.2.3+ (build 0.4.11 onward)

## Affects Versions Correction (Step 3)

Issue is scoped to stream 2.2.x per summary suffix `[rhtpa-2.2]`.

Current Affects Versions: `RHTPA 2.0.0` (incorrect -- no 2.0.x stream exists)

Proposed Affects Versions: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`

These are the versions in the 2.2.x stream that shipped quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but the version impact analysis shows that stream **2.1.x** is also fully affected (all versions ship quinn-proto 0.11.9, which is within the vulnerable range). The upstream branch `release/0.3.z` does NOT have the fix.

Cross-stream impact comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks are created for stream 2.1.x (see remediation.md).
