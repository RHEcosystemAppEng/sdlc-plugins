# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Supportability Matrix Source

- Stream 2.1.x: loaded from rhtpa-release.0.3.z security-matrix.md
- Stream 2.2.x: loaded from rhtpa-release.0.4.z security-matrix.md
- Matrix Last-Updated: 2026-06-28T10:00:00Z (within 14-day freshness window as of triage date)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source-level dependency)
Repository: backend (rhtpa-backend)
Lock file: Cargo.lock

quinn-proto is a Cargo dependency of the backend workspace. The exact dependency
chain (direct vs. transitive) and profile/scope would be determined by inspecting
Cargo.toml and Cargo.lock at the pinned commits. Based on the component label
(pscomponent:org/rhtpa-server), quinn-proto is used for QUIC transport in the
server component, indicating a production (runtime) dependency.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | `release/0.4.z` | 0.11.14 (at v0.4.12) | YES |

- **Stream 2.2.x**: upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fix). Remediation is a dependency bump + downstream propagation.
- **Stream 2.1.x**: upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation requires an upstream backport + downstream propagation.

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Issue stream scope**: 2.2.x -- Steps 3-4 apply only to 2.2.x versions
- **Cross-stream impact**: stream 2.1.x is also affected (Case A applies)
